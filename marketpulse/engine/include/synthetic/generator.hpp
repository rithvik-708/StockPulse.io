#pragma once

#include "core/types.hpp"
#include <random>
#include <string>

namespace marketpulse {

class SyntheticMarketGenerator {
public:
    SyntheticMarketGenerator(std::string symbol, double initial_price, uint32_t seed = 42);
    MarketEvent generate_event();

private:
    std::string symbol_;
    double current_price_;
    uint64_t order_sequence_{1};
    std::mt19937 rng_;
    std::normal_distribution<double> price_delta_dist_{0.0, 0.25};
    std::uniform_real_distribution<double> spread_offset_dist_{0.05, 1.50};
    std::uniform_real_distribution<double> qty_dist_{0.01, 5.0};
    std::bernoulli_distribution side_dist_{0.5};
};

} // namespace marketpulse
