cmake_minimum_required(VERSION 3.22)
project(MarketEngine VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Quant-grade low-latency flags
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -march=native -DNDEBUG -flto -fno-omit-frame-pointer")

find_package(PkgConfig REQUIRED)
pkg_check_modules(RDKAFKA REQUIRED rdkafka++)

include_directories(
    include
    ${RDKAFKA_INCLUDE_DIRS}
)

add_executable(market-engine
    src/orderbook/orderbook.cpp
    src/networking/kafka_producer.cpp
    src/synthetic/generator.cpp
    src/main.cpp
)

target_link_libraries(market-engine PRIVATE
    ${RDKAFKA_LIBRARIES}
    pthread
)
