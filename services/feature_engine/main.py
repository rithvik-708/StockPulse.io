import json
import os
import numpy as np
from collections import deque
from confluent_kafka import Consumer, Producer

KAFKA_BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVERS") or os.getenv("KAFKA_BROKER", "localhost:9092")

class RollingIndicators:
    def __init__(self, window_size=20):
        self.window = window_size
        self.prices = deque(maxlen=window_size)
        self.volumes = deque(maxlen=window_size)

    def update(self, price: float, volume: float):
        self.prices.append(price)
        self.volumes.append(volume)

    def calculate(self):
        if len(self.prices) < 2:
            return None
        
        prices_arr = np.array(self.prices)
        vols_arr = np.array(self.volumes)

        # VWAP
        vwap = np.sum(prices_arr * vols_arr) / np.sum(vols_arr) if np.sum(vols_arr) > 0 else prices_arr[-1]
        
        # 20-tick EMA approximation
        alpha = 2 / (len(self.prices) + 1)
        ema = prices_arr[-1] * alpha + (np.mean(prices_arr[:-1]) if len(prices_arr) > 1 else prices_arr[-1]) * (1 - alpha)
        
        # Rolling Volatility (Standard Deviation of returns)
        returns = np.diff(prices_arr) / prices_arr[:-1]
        volatility = np.std(returns) if len(returns) > 1 else 0.0
        
        # Momentum (Price delta over window)
        momentum = prices_arr[-1] - prices_arr[0]

        return {
            "vwap": float(vwap),
            "ema_20": float(ema),
            "volatility": float(volatility),
            "momentum": float(momentum)
        }

def get_kafka_clients():
    import time
    retries = 10
    while retries > 0:
        try:
            consumer = Consumer({
                'bootstrap.servers': KAFKA_BROKER,
                'group.id': 'feature-engine-group',
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
    
    consumer.subscribe(['market.normalized'])
    indicators = {"BTCUSDT": RollingIndicators(window_size=20)}

    print("Starting Feature Engine...")
    
    try:
        while True:
            msg = consumer.poll(0.1)
            if msg is None:
                continue
            if msg.error():
                print(f"Kafka Error: {msg.error()}")
                continue

            payload = json.loads(msg.value().decode('utf-8'))
            symbol = payload['symbol']
            mid_price = payload['mid']
            total_vol = payload.get('volume_bid', 1.0) + payload.get('volume_ask', 1.0) # Approximate L1 volume

            if symbol not in indicators:
                indicators[symbol] = RollingIndicators()
            
            ind = indicators[symbol]
            ind.update(mid_price, total_vol)
            
            features = ind.calculate()
            if features:
                feature_payload = {
                    "symbol": symbol,
                    "timestamp_ns": payload['ts'],
                    **features
                }
                producer.produce('market.features', json.dumps(feature_payload).encode('utf-8'))
                producer.poll(0)

    except KeyboardInterrupt:
        print("Shutting down Feature Engine.")
    finally:
        consumer.close()
        producer.flush()

if __name__ == "__main__":
    main()
