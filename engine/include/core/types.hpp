#pragma once
#include <string>

namespace stockpulse {

struct MarketEvent {
    std::string symbol;
    double price;
    double size;
    bool is_bid;
    uint64_t timestamp_ns;
};

struct L1Tick {
    std::string symbol;
    double bid;
    double ask;
    double spread;
    double mid;
    double imbalance;
    uint64_t ts;
    uint64_t lat_ns;
};

} // namespace stockpulse
