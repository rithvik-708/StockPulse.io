#pragma once

#include "core/types.hpp"
#include <map>
#include <list>
#include <unordered_map>
#include <optional>
#include <string>

namespace stockpulse {

class LimitOrderBook {
public:
    struct Level {
        double price;
        double total_volume{0.0};
        std::list<Order> order_queue;
    };

    using OrderIterator = std::list<Order>::iterator;
    
    struct OrderLocation {
        double price;
        Side side;
        OrderIterator iter;
    };

    explicit LimitOrderBook(std::string symbol);

    bool process_event(const MarketEvent& event);
    [[nodiscard]] std::optional<L1MarketTick> get_l1_snapshot(uint64_t receive_time_ns) const;

private:
    void add_order(const MarketEvent& event);
    void cancel_order(uint64_t order_id);
    void modify_order(const MarketEvent& event);

    std::string symbol_;
    
    // Price-time priority ladders
    // Asks sorted ascending (lowest ask first), Bids sorted descending (highest bid first)
    std::map<double, Level, std::greater<double>> bids_;
    std::map<double, Level, std::less<double>> asks_;

    // O(1) pointer map for cancels and modifications
    std::unordered_map<uint64_t, OrderLocation> order_locator_;
};

} // namespace stockpulse
