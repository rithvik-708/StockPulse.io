#include "networking/binance_client.hpp"
#include <iostream>
#include <nlohmann/json.hpp>
#include <chrono>
#include <openssl/ssl.h>
#include <openssl/err.h>
#include <boost/core/ignore_unused.hpp>

namespace marketpulse {

BinanceClient::BinanceClient(const std::string& host, const std::string& port, const std::string& path)
    : host_(host), port_(port), path_(path),
      ctx_(boost::asio::ssl::context::tlsv12_client),
      resolver_(ioc_),
      ws_(ioc_, ctx_) {
    // Optionally configure ctx_ (e.g., verifying certs, but for Binance we can skip for simplicity)
}

BinanceClient::~BinanceClient() {}

void BinanceClient::set_message_callback(MessageCallback cb) {
    callback_ = std::move(cb);
}

void BinanceClient::run() {
    resolver_.async_resolve(host_, port_,
        boost::beast::bind_front_handler(&BinanceClient::on_resolve, this));
    ioc_.run();
}

void BinanceClient::on_resolve(boost::beast::error_code ec, boost::asio::ip::tcp::resolver::results_type results) {
    if (ec) {
        std::cerr << "Resolve error: " << ec.message() << "\n";
        return;
    }
    boost::asio::async_connect(
        boost::beast::get_lowest_layer(ws_),
        results,
        boost::beast::bind_front_handler(&BinanceClient::on_connect, this));
}

void BinanceClient::on_connect(boost::beast::error_code ec, boost::asio::ip::tcp::resolver::results_type::endpoint_type ep) {
    if (ec) {
        std::cerr << "Connect error: " << ec.message() << "\n";
        return;
    }
    if (!SSL_set_tlsext_host_name(ws_.next_layer().native_handle(), host_.c_str())) {
        boost::beast::error_code ec2{static_cast<int>(::ERR_get_error()), boost::asio::error::get_ssl_category()};
        std::cerr << "SNI error: " << ec2.message() << "\n";
        return;
    }
    ws_.next_layer().async_handshake(boost::asio::ssl::stream_base::client,
        boost::beast::bind_front_handler(&BinanceClient::on_ssl_handshake, this));
}

void BinanceClient::on_ssl_handshake(boost::beast::error_code ec) {
    if (ec) {
        std::cerr << "SSL Handshake error: " << ec.message() << "\n";
        return;
    }
    std::string host_port = host_ + ":" + port_;
    ws_.async_handshake(host_port, path_,
        boost::beast::bind_front_handler(&BinanceClient::on_handshake, this));
}

void BinanceClient::on_handshake(boost::beast::error_code ec) {
    if (ec) {
        std::cerr << "WebSocket Handshake error: " << ec.message() << "\n";
        return;
    }
    do_read();
}

void BinanceClient::do_read() {
    ws_.async_read(buffer_,
        boost::beast::bind_front_handler(&BinanceClient::on_read, this));
}

void BinanceClient::on_read(boost::beast::error_code ec, std::size_t bytes_transferred) {
    boost::ignore_unused(bytes_transferred);
    if (ec) {
        std::cerr << "Read error: " << ec.message() << "\n";
        return;
    }

    auto t_receive_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(
        std::chrono::system_clock::now().time_since_epoch()).count();

    std::string payload = boost::beast::buffers_to_string(buffer_.data());
    buffer_.consume(buffer_.size());
    std::cout << "Received payload: " << payload.substr(0, 50) << "...\n";

    try {
        auto j = nlohmann::json::parse(payload);
        std::vector<MarketEvent> events;

        if (j.contains("bids")) {
            for (const auto& bid : j["bids"]) {
                double price = std::stod(bid[0].get<std::string>());
                double size = std::stod(bid[1].get<std::string>());
                events.push_back({"BTCUSDT", price, size, true, static_cast<uint64_t>(t_receive_ns)});
            }
        }
        if (j.contains("asks")) {
            for (const auto& ask : j["asks"]) {
                double price = std::stod(ask[0].get<std::string>());
                double size = std::stod(ask[1].get<std::string>());
                events.push_back({"BTCUSDT", price, size, false, static_cast<uint64_t>(t_receive_ns)});
            }
        }

        if (callback_) {
            callback_(events, t_receive_ns);
        }
    } catch (const std::exception& e) {
        std::cerr << "JSON parse error: " << e.what() << "\n";
    }

    do_read();
}

} // namespace marketpulse
