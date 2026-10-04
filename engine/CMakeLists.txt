cmake_minimum_required(VERSION 3.22)
project(MarketEngine VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -march=native -DNDEBUG -flto")

find_package(PkgConfig REQUIRED)
# Optional rdkafka to prevent cmake failures if missing
pkg_check_modules(RDKAFKA rdkafka++)

include(FetchContent)

# Fetch nlohmann JSON for rapid payload parsing
FetchContent_Declare(json URL https://github.com/nlohmann/json/releases/download/v3.11.2/json.tar.xz)
FetchContent_MakeAvailable(json)

# Fetch prometheus-cpp
FetchContent_Declare(
  prometheus-cpp
  GIT_REPOSITORY https://github.com/jupp0r/prometheus-cpp.git
  GIT_TAG v1.1.0
)
set(ENABLE_TESTING OFF CACHE BOOL "Disable prometheus-cpp tests")
FetchContent_MakeAvailable(prometheus-cpp)

# Locate system Boost (Requires: sudo apt install libboost-all-dev)
find_package(Boost REQUIRED COMPONENTS system thread)
find_package(OpenSSL REQUIRED)

include_directories(include)
if(RDKAFKA_FOUND)
    include_directories(${RDKAFKA_INCLUDE_DIRS})
endif()

add_executable(market-engine
    src/orderbook/orderbook.cpp
    src/networking/kafka_producer.cpp
    src/networking/binance_client.cpp
    src/main.cpp
)

target_link_libraries(market-engine PRIVATE
    Boost::system
    Boost::thread
    OpenSSL::SSL
    OpenSSL::Crypto
    nlohmann_json::nlohmann_json
    prometheus-cpp::pull
    prometheus-cpp::core
    pthread
)
if(RDKAFKA_FOUND)
    target_link_libraries(market-engine PRIVATE ${RDKAFKA_LIBRARIES})
endif()
