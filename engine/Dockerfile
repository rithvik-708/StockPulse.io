# Stage 1: Build
FROM ubuntu:22.04 AS builder
RUN apt-get update && apt-get install -y \
    cmake \
    g++ \
    libssl-dev \
    librdkafka-dev \
    libboost-all-dev \
    libcurl4-openssl-dev \
    zlib1g-dev \
    git \
    curl \
    tar \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . .
RUN mkdir -p build && cd build && cmake -DCMAKE_BUILD_TYPE=Release .. && make -j$(nproc)

# Stage 2: Runtime
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y \
    librdkafka1 \
    librdkafka++1 \
    libssl3 \
    libcurl4 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY --from=builder /app/build/market-engine .
EXPOSE 8080
CMD ["./market-engine", "pulse-kafka:9094"]
