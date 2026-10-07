import json
import os
import time
import psycopg
import redis
from confluent_kafka import Consumer

KAFKA_BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVERS") or os.getenv("KAFKA_BROKER", "localhost:9092")
PG_DSN = os.getenv("PG_DSN", "postgresql://quant:quantpassword@localhost:5433/stockpulse")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

class StorageSink:
    def __init__(self):
        self._init_connections()
        self.event_buffer = []
        self.feature_buffer = []
        self.last_flush = time.time()
        self.last_log_time = 0

    def _init_connections(self):
        retries = 10
        while retries > 0:
            try:
                self.r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
                self.r.ping()
                self.pg_conn = psycopg.connect(PG_DSN, autocommit=True)
                
                self.consumer = Consumer({
                    'bootstrap.servers': KAFKA_BROKER,
                    'group.id': 'storage-sink-group',
                    'auto.offset.reset': 'latest'
                })
                self.consumer.subscribe(['market.normalized', 'market.features'])
                print(f"✅ Successfully connected to Redis, Postgres, and Kafka ({KAFKA_BROKER})")
                break
            except Exception as e:
                print(f"⚠️ Connection failed: {e}. Retrying in 5 seconds... ({retries} left)")
                retries -= 1
                time.sleep(5)
        if retries == 0:
            raise Exception("❌ Fatal: Failed to initialize connections.")

    def process_messages(self):
        print("Starting Storage Sink (Redis + Postgres Batching)...")
        pipeline = self.r.pipeline()

        try:
            while True:
                msg = self.consumer.poll(0.1)
                
                if msg is not None and not msg.error():
                    topic = msg.topic()
                    payload = json.loads(msg.value().decode('utf-8'))
                    symbol = payload['symbol']

                    # 1. Push to Redis Hot State (60s TTL)
                    if topic == 'market.normalized':
                        pipeline.setex(f"market:l1:{symbol}", 60, json.dumps(payload))
                        self.event_buffer.append((
                            payload['ts'], symbol, payload['bid'], payload['ask'],
                            payload['spread'], payload['mid'], payload['imbalance'], payload['lat_ns']
                        ))
                    elif topic == 'market.features':
                        pipeline.setex(f"market:features:{symbol}", 60, json.dumps(payload))
                        self.feature_buffer.append((
                            payload['timestamp_ns'], symbol, payload['vwap'],
                            payload['ema_20'], payload['volatility'], payload['momentum']
                        ))
                    
                    pipeline.publish("market_updates", json.dumps(payload))
                    pipeline.execute()
                    
                    if time.time() - self.last_log_time > 5.0:
                        print(f"[{topic}] Wrote {symbol} -> Redis (ts={payload.get('ts', payload.get('timestamp_ns', 0))})")
                        self.last_log_time = time.time()

                # 2. Batch Insert to PostgreSQL (1000 items or 1 second)
                if len(self.event_buffer) >= 1000 or (time.time() - self.last_flush > 1.0 and self.event_buffer):
                    self._flush_postgres()

        except KeyboardInterrupt:
            self._flush_postgres()
            print("Shutting down Storage Sink.")
        finally:
            self.consumer.close()
            self.pg_conn.close()

    def _flush_postgres(self):
        if not self.event_buffer and not self.feature_buffer:
            return

        try:
            with self.pg_conn.cursor() as cur:
                if self.event_buffer:
                    cur.executemany("""
                        INSERT INTO market_events 
                        (timestamp_ns, symbol, best_bid, best_ask, spread, mid_price, imbalance, latency_ns)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, self.event_buffer)
                
                if self.feature_buffer:
                    cur.executemany("""
                        INSERT INTO market_features 
                        (timestamp_ns, symbol, vwap, ema_20, volatility, momentum)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, self.feature_buffer)
        except Exception as e:
            print(f"Postgres batch insert failed: {e}")

        self.event_buffer.clear()
        self.feature_buffer.clear()
        self.last_flush = time.time()

if __name__ == "__main__":
    sink = StorageSink()
    sink.process_messages()
