import os
import sys
import redis
import psycopg
from confluent_kafka import Consumer

print("--- StockPulse.io End-to-End Pipeline Health Check ---")

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
PG_DSN = os.getenv("PG_DSN", "postgresql://quant:quantpassword@localhost:5433/stockpulse")
KAFKA_BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

status = True

# 1. Check Redis
try:
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    r.ping()
    print("[PASS] Redis is reachable.")
    
    # Check keys
    keys = r.keys("market:l1:*")
    if keys:
        print(f"[PASS] Redis contains L1 data: {len(keys)} symbols.")
    else:
        print("[FAIL] Redis contains NO L1 data.")
        status = False
        
    features = r.keys("market:features:*")
    if features:
        print(f"[PASS] Redis contains Features data: {len(features)} symbols.")
    else:
        print("[FAIL] Redis contains NO Features data.")
        status = False
        
except Exception as e:
    print(f"[FAIL] Redis error: {e}")
    status = False

# 2. Check Postgres
try:
    conn = psycopg.connect(PG_DSN, autocommit=True)
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM market_events")
        cnt = cur.fetchone()[0]
        print(f"[PASS] Postgres is reachable. L1 Events in DB: {cnt}")
    conn.close()
except Exception as e:
    print(f"[FAIL] Postgres error: {e}")
    status = False

# 3. Check Kafka
try:
    consumer = Consumer({
        'bootstrap.servers': KAFKA_BROKER,
        'group.id': 'health-check-group',
        'auto.offset.reset': 'latest'
    })
    topics = consumer.list_topics(timeout=5).topics
    if 'market.normalized' in topics and 'market.features' in topics:
        print("[PASS] Kafka is reachable and topics exist.")
    else:
        print(f"[WARN] Kafka is reachable, but missing topics. Topics: {list(topics.keys())}")
        status = False
except Exception as e:
    print(f"[FAIL] Kafka error: {e}")
    status = False

print("--- Health Check Complete ---")
sys.exit(0 if status else 1)
