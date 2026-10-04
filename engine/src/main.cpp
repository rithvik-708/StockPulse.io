#include "core/types.hpp"
#include "orderbook/orderbook.hpp"
#include "networking/kafka_producer.hpp"
#include "networking/binance_client.hpp"

#include <iostream>
#include <vector>
#include <memory>
#include <prometheus/exposer.h>
#include <prometheus/registry.h>
#include <prometheus/counter.h>
#include <prometheus/histogram.h>

int main(int argc, char* argv[]) {
    std::setvbuf(stdout, NULL, _IONBF, 0);
    std::setvbuf(stderr, NULL, _IONBF, 0);
    std::string kafka_broker = (argc > 1) ? argv[1] : "localhost:9094";

    std::cout << "Starting Live Market Ingestion (Day 5)...\n";

    // Setup Prometheus Exposer
    using namespace prometheus;
    Exposer exposer{"0.0.0.0:8080"};
    auto registry = std::make_shared<Registry>();

    auto& event_counter = BuildCounter()
        .Name("marketpulse_events_total")
        .Help("Total market events processed")
        .Register(*registry)
        .Add({{"symbol", "BTCUSDT"}});

    auto& latency_histogram = BuildHistogram()
        .Name("marketpulse_latency_microseconds")
        .Help("Processing latency in microseconds")
        .Register(*registry)
        .Add({}, Histogram::BucketBoundaries{0.5, 1.0, 2.0, 5.0, 10.0, 50.0});

    exposer.RegisterCollectable(registry);

    marketpulse::LimitOrderBook order_book("BTCUSDT");
    marketpulse::LowLatencyKafkaProducer producer(kafka_broker, "market.normalized");

    // The Binance WebSocket Client handles the ASIO event loop and parses L2 payload JSON 
    // down to marketpulse::MarketEvent arrays, then invokes the callback.
    marketpulse::BinanceClient ws_client("stream.binance.com", "9443", "/ws/btcusdt@depth5@100ms");

    ws_client.set_message_callback([&](const std::vector<marketpulse::MarketEvent>& events, uint64_t t_receive_ns) {
        for (const auto& ev : events) {
            order_book.process_event(ev);
        }

        auto l1_tick = order_book.get_l1_snapshot(t_receive_ns);
        if (l1_tick) {
            std::cout << "Publishing tick to Kafka: mid=" << l1_tick->mid << "\n";
            producer.publish_l1_tick(*l1_tick);
            
            // Prometheus metrics observation
            event_counter.Increment(events.size());
            latency_histogram.Observe(l1_tick->lat_ns / 1000.0);
        } else {
            std::cout << "Orderbook snapshot empty (waiting for both bids and asks)...\n";
        }
        producer.poll(0);
    });

    std::cout << "Connected to Binance. Streaming live L1 ticks to Kafka...\n";
    ws_client.run(); // Blocks and runs the network loop

    return 0;
}
