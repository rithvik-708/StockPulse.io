import json
import time
import random
import os
from confluent_kafka import Producer

KAFKA_BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVERS") or os.getenv("KAFKA_BROKER", "localhost:9092")

def generate_mock_ticks():
    if os.getenv("MOCK_DATA", "").lower() not in ("1", "true", "yes"):
        print("MOCK_DATA=true is not set in environment. Exiting mock feed to prevent accidental mock data pollution.")
        return

    producer = Producer({'bootstrap.servers': KAFKA_BROKER})
    symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
    base_prices = {"BTCUSDT": 98500.0, "ETHUSDT": 3450.0, "SOLUSDT": 195.0}

    print(f"📡 Mock Market Feeder started on Kafka broker: {KAFKA_BROKER}")
    print("Streaming synthetic L1 order book updates for BTC, ETH, SOL... (Press Ctrl+C to stop)")

    try:
        while True:
            for sym in symbols:
                base_prices[sym] += random.uniform(-2.5, 2.5)
                mid = round(base_prices[sym], 2)
                spread = round(random.uniform(0.5, 2.0), 2)
                bid = round(mid - spread / 2, 2)
                ask = round(mid + spread / 2, 2)
                vol_bid = round(random.uniform(5.0, 50.0), 2)
                vol_ask = round(random.uniform(5.0, 50.0), 2)
                imbalance = round((vol_bid - vol_ask) / (vol_bid + vol_ask), 4)

                tick = {
                    "symbol": sym,
                    "bid": bid,
                    "ask": ask,
                    "spread": spread,
                    "mid": mid,
                    "imbalance": imbalance,
                    "volume_bid": vol_bid,
                    "volume_ask": vol_ask,
                    "ts": time.time_ns(),
                    "lat_ns": random.randint(1500, 4500),
                    "data_mode": "mock"
                }

                producer.produce("market.normalized", json.dumps(tick).encode('utf-8'))
            
            producer.poll(0)
            time.sleep(0.1) # 10 ticks per second
    except KeyboardInterrupt:
        print("\nStopping Mock Market Feeder.")
    finally:
        producer.flush()

if __name__ == "__main__":
    generate_mock_ticks()
