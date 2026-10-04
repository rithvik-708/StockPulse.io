#pragma once

#include "core/types.hpp"
#include <string>
#include <memory>
#include <librdkafka/rdkafkacpp.h>

namespace marketpulse {

class LowLatencyKafkaProducer : public RdKafka::DeliveryReportCb {
public:
    explicit LowLatencyKafkaProducer(const std::string& brokers, const std::string& topic);
    ~LowLatencyKafkaProducer() override;

    bool publish_l1_tick(const L1MarketTick& tick);
    void poll(int timeout_ms = 0);
    void dr_cb(RdKafka::Message& message) override;

private:
    std::string topic_name_;
    std::unique_ptr<RdKafka::Producer> producer_;
    std::unique_ptr<RdKafka::Topic> topic_;
};

} // namespace marketpulse
