import json
import os
from confluent_kafka import Consumer, Producer

KAFKA_BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVERS") or os.getenv("KAFKA_BROKER", "localhost:9092")
IMBALANCE_THRESHOLD = 0.20
MOMENTUM_THRESHOLD = 0.0

def evaluate_strategy(features: dict) -> str:
    imbalance = features.get('imbalance', 0.0) # Assume storage sink passes this, or use EMA/VWAP divergence
    momentum = features.get('momentum', 0.0)
    
    if imbalance > IMBALANCE_THRESHOLD and momentum > MOMENTUM_THRESHOLD:
        return "LONG"
    elif imbalance < -IMBALANCE_THRESHOLD and momentum < -MOMENTUM_THRESHOLD:
        return "SHORT"
    return "HOLD"

def get_kafka_clients():
    import time
    retries = 10
    while retries > 0:
        try:
            consumer = Consumer({
                'bootstrap.servers': KAFKA_BROKER,
                'group.id': 'signal-engine-group',
                'auto.offset.reset': 'latest'
            })
            producer = Producer({'bootstrap.servers': KAFKA_BROKER})
            return consumer, producer
        except Exception as e:
            print(f"⚠️ Kafka connection failed: {e}. Retrying in 5s... ({retries} left)")
            retries -= 1
            time.sleep(5)
    raise Exception("❌ Fatal: Failed to connect to Kafka.")

def main():
    consumer, producer = get_kafka_clients()
    
    consumer.subscribe(['market.features'])
    print("Starting Quantitative Signal Engine...")
    
    try:
        while True:
            msg = consumer.poll(0.1)
            if msg is None or msg.error():
                continue

            features = json.loads(msg.value().decode('utf-8'))
            signal = evaluate_strategy(features)
            
            signal_payload = {
                "symbol": features['symbol'],
                "timestamp_ns": features['timestamp_ns'],
                "signal": signal,
                "strategy": "ImbalanceMomentum",
                "confidence": abs(features.get('momentum', 0)) # Naive confidence metric
            }
            
            producer.produce('market.signals', json.dumps(signal_payload).encode('utf-8'))
            producer.poll(0)
            
            # Optional: Log actionable signals
            if signal != "HOLD":
                print(f"[{features['symbol']}] {signal} SIGNAL GENERATED")

    except KeyboardInterrupt:
        print("Shutting down Signal Engine.")
    finally:
        consumer.close()
        producer.flush()

if __name__ == "__main__":
    main()
