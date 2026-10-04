#!/bin/bash
echo "Injecting 100k TPS synthetic load via market-engine..."
# The actual market-engine will handle the binance connection and high throughput
echo "Running the system for 10 seconds..."
sleep 10

echo "Simulating Kafka broker crash (ruthlessly killing pulse-kafka)..."
docker kill pulse-kafka
sleep 5

echo "Restarting Kafka broker..."
docker start pulse-kafka

echo "Verify in the Docker logs that the Python consumers automatically re-establish connection and resume consumption."
