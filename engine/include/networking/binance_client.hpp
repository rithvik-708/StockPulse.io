#pragma once
#include <string>
#include <functional>
#include <vector>
#include "core/types.hpp"
#include <boost/beast/core.hpp>
#include <boost/beast/websocket.hpp>
#include <boost/beast/websocket/ssl.hpp>
#include <boost/asio/connect.hpp>
#include <boost/asio/ip/tcp.hpp>
#include <boost/asio/ssl/stream.hpp>
#include <boost/asio/ssl/context.hpp>

namespace marketpulse {

class BinanceClient {
public:
    using MessageCallback = std::function<void(const std::vector<MarketEvent>&, uint64_t)>;

    BinanceClient(const std::string& host, const std::string& port, const std::string& path);
    ~BinanceClient();

    void set_message_callback(MessageCallback cb);
    void run();

private:
    void on_resolve(boost::beast::error_code ec, boost::asio::ip::tcp::resolver::results_type results);
    void on_connect(boost::beast::error_code ec, boost::asio::ip::tcp::resolver::results_type::endpoint_type ep);
    void on_ssl_handshake(boost::beast::error_code ec);
    void on_handshake(boost::beast::error_code ec);
    void do_read();
    void on_read(boost::beast::error_code ec, std::size_t bytes_transferred);

    std::string host_;
    std::string port_;
    std::string path_;
    
    boost::asio::io_context ioc_;
    boost::asio::ssl::context ctx_;
    boost::asio::ip::tcp::resolver resolver_;
    boost::beast::websocket::stream<boost::asio::ssl::stream<boost::asio::ip::tcp::socket>> ws_;
    boost::beast::flat_buffer buffer_;
    
    MessageCallback callback_;
};

} // namespace marketpulse
