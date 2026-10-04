#include "orderbook/orderbook.hpp"
#include <cstring>
#include <iostream>

namespace marketpulse {

LimitOrderBook::LimitOrderBook(std::string symbol) : symbol_(std::move(symbol)) {
    order_locator_.reserve(100'000);
}

bool LimitOrderBook::process_event(const MarketEvent& event) {
    switch (event.action) {
        case Action::ADD:
            add_order(event);
            return true;
        case Action::CANCEL:
            cancel_order(event.event_id);
            return true;
        case Action::MODIFY:
            modify_order(event);
            return true;
        default:
            return false;
    }
}

void LimitOrderBook::add_order(const MarketEvent& event) {
    if (event.side == Side::BUY) {
        auto& level = bids_[event.price];
        level.price = event.price;
        level.total_volume += event.quantity;
        level.order_queue.push_back({event.event_id, event.side, event.price, event.quantity, event.timestamps.t_receive_ns});
        
        order_locator_[event.event_id] = {event.price, event.side, std::prev(level.order_queue.end())};
    } else {
        auto& level = asks_[event.price];
        level.price = event.price;
        level.total_volume += event.quantity;
        level.order_queue.push_back({event.event_id, event.side, event.price, event.quantity, event.timestamps.t_receive_ns});
        
        order_locator_[event.event_id] = {event.price, event.side, std::prev(level.order_queue.end())};
    }
}

void LimitOrderBook::cancel_order(uint64_t order_id) {
    auto it = order_locator_.find(order_id);
    if (it == order_locator_.end()) return;

    const auto& loc = it->second;
    if (loc.side == Side::BUY) {
        auto level_it = bids_.find(loc.price);
        if (level_it != bids_.end()) {
            level_it->second.total_volume -= loc.iter->quantity;
            level_it->second.order_queue.erase(loc.iter);
            if (level_it->second.order_queue.empty()) {
                bids_.erase(level_it);
            }
        }
    } else {
        auto level_it = asks_.find(loc.price);
        if (level_it != asks_.end()) {
            level_it->second.total_volume -= loc.iter->quantity;
            level_it->second.order_queue.erase(loc.iter);
            if (level_it->second.order_queue.empty()) {
                asks_.erase(level_it);
            }
        }
    }
    order_locator_.erase(it);
}

void LimitOrderBook::modify_order(const MarketEvent& event) {
    cancel_order(event.event_id);
    add_order(event);
}

std::optional<L1MarketTick> LimitOrderBook::get_l1_snapshot(uint64_t receive_time_ns) const {
    if (bids_.empty() || asks_.empty()) {
        return std::nullopt;
    }

    const auto best_bid_it = bids_.begin();
    const auto best_ask_it = asks_.begin();

    const double best_bid = best_bid_it->first;
    const double best_ask = best_ask_it->first;
    const double vol_bid = best_bid_it->second.total_volume;
    const double vol_ask = best_ask_it->second.total_volume;

    const double spread = best_ask - best_bid;
    const double mid = (best_bid + best_ask) * 0.5;
    const double total_top_volume = vol_bid + vol_ask;
    const double imbalance = (total_top_volume > 0.0) ? (vol_bid - vol_ask) / total_top_volume : 0.0;

    L1MarketTick tick;
    std::strncpy(tick.symbol, symbol_.c_str(), sizeof(tick.symbol) - 1);
    tick.timestamp_ns = now_nanoseconds();
    tick.best_bid = best_bid;
    tick.best_ask = best_ask;
    tick.spread = spread;
    tick.mid_price = mid;
    tick.volume_bid = vol_bid;
    tick.volume_ask = vol_ask;
    tick.book_imbalance = imbalance;
    tick.processing_latency_ns = tick.timestamp_ns - receive_time_ns;

    return tick;
}

} // namespace marketpulse
