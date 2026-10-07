#pragma once
#include "core/types.hpp"
#include <string>
#include <optional>
#include <map>

namespace stockpulse {

class LimitOrderBook {
public:
    explicit LimitOrderBook(std::string symbol);

    void process_event(const MarketEvent& event);
    std::optional<L1Tick> get_l1_snapshot(uint64_t current_ts_ns) const;

private:
    std::string symbol_;
    std::map<double, double, std::greater<double>> bids_;
    std::map<double, double, std::less<double>> asks_;
};

} // namespace stockpulse
