#include "networking/kafka_producer.hpp"
#include <iostream>
#include <nlohmann/json.hpp>
#include <librdkafka/rdkafkacpp.h>

namespace stockpulse {

LowLatencyKafkaProducer::LowLatencyKafkaProducer(const std::string& brokers, const std::string& topic)
    : topic_(topic) {
    std::string errstr;
    RdKafka::Conf *conf = RdKafka::Conf::create(RdKafka::Conf::CONF_GLOBAL);
    conf->set("bootstrap.servers", brokers, errstr);
    conf->set("debug", "broker,topic,msg", errstr);
    
    RdKafka::Producer *producer = RdKafka::Producer::create(conf, errstr);
    if (!producer) {
        std::cerr << "Failed to create producer: " << errstr << std::endl;
    } else {
        impl_ = producer;
        std::cout << "Kafka Producer initialized for topic: " << topic << " at " << brokers << "\n";
    }
    delete conf;
}

LowLatencyKafkaProducer::~LowLatencyKafkaProducer() {
    if (impl_) {
        auto* producer = static_cast<RdKafka::Producer*>(impl_);
        producer->flush(5000);
        delete producer;
    }
}

void LowLatencyKafkaProducer::publish_l1_tick(const L1Tick& tick) {
    if (!impl_) return;
    auto* producer = static_cast<RdKafka::Producer*>(impl_);

    nlohmann::json j = {
        {"symbol", tick.symbol},
        {"bid", tick.bid},
        {"ask", tick.ask},
        {"spread", tick.spread},
        {"mid", tick.mid},
        {"imbalance", tick.imbalance},
        {"ts", tick.ts},
        {"lat_ns", tick.lat_ns},
        {"data_mode", "live"}
    };
    
    std::string payload = j.dump();
    RdKafka::ErrorCode err = producer->produce(
        topic_, RdKafka::Topic::PARTITION_UA,
        RdKafka::Producer::RK_MSG_COPY,
        const_cast<char*>(payload.c_str()), payload.size(),
        NULL, 0, 0, NULL
    );
    
    if (err != RdKafka::ERR_NO_ERROR) {
        std::cerr << "Failed to produce to Kafka: " << RdKafka::err2str(err) << std::endl;
    }
}

void LowLatencyKafkaProducer::poll(int timeout_ms) {
    if (impl_) {
        static_cast<RdKafka::Producer*>(impl_)->poll(timeout_ms);
    }
}

} // namespace stockpulse
