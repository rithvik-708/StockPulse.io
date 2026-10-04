#include "core/types.hpp"
#include "orderbook/orderbook.hpp"
#include "networking/kafka_producer.hpp"
#include "synthetic/generator.hpp"

#include <iostream>
#include <vector>
#include <chrono>
#include <iomanip>
#include <algorithm>
#include <string>

int main(int argc, char* argv[]) {
    std::string kafka_broker = (argc > 1) ? argv[1] : "localhost:9094";
    std::string kafka_topic  = (argc > 2) ? argv[2] : "market.normalized";

    const size_t TOTAL_EVENTS = 200'000;
    std::cout << "========================================================\n"
              << "MarketPulse Core Engine - Day 1 Initialization\n"
              << "Connecting to Kafka: " << kafka_broker << " [Topic: " << kafka_topic << "]\n"
              << "Streaming Target: " << TOTAL_EVENTS << " deterministic events\n"
              << "========================================================\n";

    marketpulse::LimitOrderBook order_book("BTCUSDT");
    marketpulse::LowLatencyKafkaProducer producer(kafka_broker, kafka_topic);
    marketpulse::SyntheticMarketGenerator generator("BTCUSDT", 98500.0, 1337);

    std::vector<double> latencies_ns;
    latencies_ns.reserve(TOTAL_EVENTS);

    const auto bench_start = std::chrono::steady_clock::now();

    for (size_t i = 0; i < TOTAL_EVENTS; ++i) {
        // 1. Ingest synthetic order
        auto event = generator.generate_event();

        // 2. Process order inside memory LOB
        event.timestamps.t_process_ns = marketpulse::now_nanoseconds();
        order_book.process_event(event);

        // 3. Extract Level 1 Derived Metrics
        auto l1_tick = order_book.get_l1_snapshot(event.timestamps.t_receive_ns);

        // 4. Stream to Kafka pipeline
        if (l1_tick) {
            producer.publish_l1_tick(*l1_tick);
            latencies_ns.push_back(static_cast<double>(l1_tick->processing_latency_ns));
        }

        if (i % 2000 == 0) {
            producer.poll(0);
        }
    }

    const auto bench_end = std::chrono::steady_clock::now();
    producer.poll(500);

    const double elapsed_sec = std::chrono::duration<double>(bench_end - bench_start).count();
    const double throughput = static_cast<double>(TOTAL_EVENTS) / elapsed_sec;

    std::sort(latencies_ns.begin(), latencies_ns.end());
    auto percentile = [&](double p) -> double {
        if (latencies_ns.empty()) return 0.0;
        size_t idx = static_cast<size_t>(p * (latencies_ns.size() - 1));
        return latencies_ns[idx] / 1'000.0; // microseconds
    };

    std::cout << "\n================ BENCHMARK RESULTS ================\n"
              << "Processed:        " << TOTAL_EVENTS << " events\n"
              << "Wall Time:        " << std::fixed << std::setprecision(4) << elapsed_sec << " s\n"
              << "Throughput:       " << std::fixed << std::setprecision(0) << throughput << " events/sec\n"
              << "Latency (P50):    " << std::setprecision(2) << percentile(0.50) << " us\n"
              << "Latency (P90):    " << percentile(0.90) << " us\n"
              << "Latency (P99):    " << percentile(0.99) << " us\n"
              << "Latency (Max):    " << (latencies_ns.empty() ? 0.0 : latencies_ns.back() / 1'000.0) << " us\n"
              << "===================================================\n";

    return 0;
}
