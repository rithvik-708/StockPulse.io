#include "synthetic/generator.hpp"
#include <cstring>

namespace stockpulse {

SyntheticMarketGenerator::SyntheticMarketGenerator(std::string symbol, double initial_price, uint32_t seed)
    : symbol_(std::move(symbol)), current_price_(initial_price), rng_(seed) {}

MarketEvent SyntheticMarketGenerator::generate_event() {
    MarketEvent ev{};
    ev.timestamps.t_receive_ns = now_nanoseconds();

    ev.event_id = order_sequence_++;
    std::strncpy(ev.symbol, symbol_.c_str(), sizeof(ev.symbol) - 1);
    ev.action = Action::ADD;
    ev.side = side_dist_(rng_) ? Side::BUY : Side::SELL;

    // Drifting random walk
    current_price_ += price_delta_dist_(rng_);
    if (current_price_ < 100.0) current_price_ = 100.0;

    double offset = spread_offset_dist_(rng_);
    ev.price = (ev.side == Side::BUY) ? (current_price_ - offset) : (current_price_ + offset);
    ev.quantity = qty_dist_(rng_);

    ev.timestamps.t_parse_ns = now_nanoseconds();
    ev.timestamps.t_validate_ns = now_nanoseconds();

    return ev;
}

} // namespace stockpulse
