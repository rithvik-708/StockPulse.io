#pragma once

#include <cstdint>
#include <chrono>
#include <string>

namespace stockpulse {

enum class Side : uint8_t {
    BUY = 0,
    SELL = 1
};

enum class Action : uint8_t {
    ADD = 0,
    MODIFY = 1,
    CANCEL = 2
};

struct Order {
    uint64_t order_id;
    Side side;
    double price;
    double quantity;
    uint64_t timestamp_ns;
};

struct EventTimestamps {
    uint64_t t_receive_ns{0};
    uint64_t t_parse_ns{0};
    uint64_t t_validate_ns{0};
    uint64_t t_process_ns{0};
    uint64_t t_publish_ns{0};

    [[nodiscard]] inline uint64_t total_latency_ns() const {
        return t_publish_ns - t_receive_ns;
    }
};

struct MarketEvent {
    uint64_t event_id;
    char symbol[16];
    Action action;
    Side side;
    double price;
    double quantity;
    EventTimestamps timestamps;
};

struct L1MarketTick {
    char symbol[16];
    uint64_t timestamp_ns;
    double best_bid;
    double best_ask;
    double spread;
    double mid_price;
    double volume_bid;
    double volume_ask;
    double book_imbalance;
    uint64_t processing_latency_ns;
};

inline uint64_t now_nanoseconds() {
    return std::chrono::duration_cast<std::chrono::nanoseconds>(
        std::chrono::steady_clock::now().time_since_epoch()
    ).count();
}

} // namespace stockpulse
