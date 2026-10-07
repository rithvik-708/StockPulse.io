#include "networking/kafka_producer.hpp"
#include <iostream>
#include <cstdio>
#include <vector>

namespace stockpulse {

LowLatencyKafkaProducer::LowLatencyKafkaProducer(const std::string& brokers, const std::string& topic_name)
    : topic_name_(topic_name) {
    std::string errstr;
    auto conf = std::unique_ptr<RdKafka::Conf>(RdKafka::Conf::create(RdKafka::Conf::CONF_GLOBAL));
    
    conf->set("bootstrap.servers", brokers, errstr);
    conf->set("queue.buffering.max.messages", "500000", errstr);
    // Low latency tunings
    conf->set("queue.buffering.max.ms", "1", errstr); 
    conf->set("batch.num.messages", "1000", errstr);
    conf->set("acks", "1", errstr);
    conf->set("compression.codec", "none", errstr);
    conf->set("dr_cb", this, errstr);

    producer_.reset(RdKafka::Producer::create(conf.get(), errstr));
    if (!producer_) {
        std::cerr << "[KAFKA ERROR] Failed to create producer: " << errstr << std::endl;
        return;
    }

    auto tconf = std::unique_ptr<RdKafka::Conf>(RdKafka::Conf::create(RdKafka::Conf::CONF_TOPIC));
    topic_.reset(RdKafka::Topic::create(producer_.get(), topic_name_, tconf.get(), errstr));
}

LowLatencyKafkaProducer::~LowLatencyKafkaProducer() {
    if (producer_) {
        producer_->flush(2000);
    }
}

void LowLatencyKafkaProducer::dr_cb(RdKafka::Message& message) {
    if (message.status() != RdKafka::Message::MSG_STATUS_NOT_PRODUCED) {
        return;
    }
    std::cerr << "[KAFKA MSG DROP] Status: " << message.errstr() << std::endl;
}

void LowLatencyKafkaProducer::poll(int timeout_ms) {
    if (producer_) producer_->poll(timeout_ms);
}

bool LowLatencyKafkaProducer::publish_l1_tick(const L1MarketTick& tick) {
    // Fast fixed-size string formatting (eliminating external heavy serializers on Day 1)
    char payload[256];
    int len = std::snprintf(
        payload, sizeof(payload),
        "{\"symbol\":\"%s\",\"ts\":%llu,\"bid\":%.2f,\"ask\":%.2f,\"spread\":%.4f,\"mid\":%.2f,\"imbalance\":%.4f,\"lat_ns\":%llu}",
        tick.symbol,
        static_cast<unsigned long long>(tick.timestamp_ns),
        tick.best_bid,
        tick.best_ask,
        tick.spread,
        tick.mid_price,
        tick.book_imbalance,
        static_cast<unsigned long long>(tick.processing_latency_ns)
    );

    if (len <= 0) return false;

    RdKafka::ErrorCode resp = producer_->produce(
        topic_.get(),
        RdKafka::Topic::PARTITION_UA,
        RdKafka::Producer::RK_MSG_COPY,
        payload,
        static_cast<size_t>(len),
        nullptr,
        nullptr
    );

    return (resp == RdKafka::ERR_NO_ERROR);
}

} // namespace stockpulse
