#include "orderbook/orderbook.hpp"

namespace marketpulse {

LimitOrderBook::LimitOrderBook(std::string symbol) : symbol_(std::move(symbol)) {}

void LimitOrderBook::process_event(const MarketEvent& event) {
    if (event.is_bid) {
        if (event.size == 0) bids_.erase(event.price);
        else bids_[event.price] = event.size;
    } else {
        if (event.size == 0) asks_.erase(event.price);
        else asks_[event.price] = event.size;
    }
}

std::optional<L1Tick> LimitOrderBook::get_l1_snapshot(uint64_t current_ts_ns) const {
    if (bids_.empty() || asks_.empty()) return std::nullopt;
    
    double best_bid = bids_.begin()->first;
    double best_ask = asks_.begin()->first;
    double vol_bid = bids_.begin()->second;
    double vol_ask = asks_.begin()->second;
    
    L1Tick tick;
    tick.symbol = symbol_;
    tick.bid = best_bid;
    tick.ask = best_ask;
    tick.spread = best_ask - best_bid;
    tick.mid = (best_bid + best_ask) / 2.0;
    tick.imbalance = (vol_bid - vol_ask) / (vol_bid + vol_ask);
    tick.ts = current_ts_ns;
    tick.lat_ns = 0; // Simulated latency
    
    return tick;
}

} // namespace marketpulse
