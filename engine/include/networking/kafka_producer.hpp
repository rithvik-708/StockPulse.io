#pragma once
#include "core/types.hpp"
#include <string>

namespace marketpulse {

class LowLatencyKafkaProducer {
public:
    LowLatencyKafkaProducer(const std::string& brokers, const std::string& topic);
    ~LowLatencyKafkaProducer();

    void publish_l1_tick(const L1Tick& tick);
    void poll(int timeout_ms);

private:
    std::string topic_;
    void* impl_ = nullptr;
};

} // namespace marketpulse
