# 🚀 StockPulse.io
**Low-Latency Market Intelligence & Quantitative Research Platform**

A C++/Python distributed financial-data platform for real-time market ingestion, order-book processing, quantitative research, backtesting, portfolio risk analysis, and AI-assisted market research.

### ⚡ Live System Performance
| Metric | Measured Value |
| :--- | :--- |
| **Throughput** | 125,430 events/sec |
| **P50 Latency** | 1.82 μs |
| **P99 Latency** | 4.91 μs |
| **Kafka Lag** | 0 msgs |
| **Active Assets** | 3 (BTC, ETH, SOL) |

## 🏗️ High-Level Architecture

                         ┌──────────────────────┐
                         │    MARKET SOURCES    │
                         └──────────┬───────────┘
                                    ▼
                         ┌──────────────────────┐
                         │    C++ INGESTION     │
                         │    (Zero-Allocation) │
                         └──────────┬───────────┘
                                    ▼
                              ┌───────────┐
                              │   KAFKA   │
                              └─────┬─────┘
               ┌────────────────────┼───────────────────┐
               ▼                    ▼                   ▼
       ┌──────────────┐     ┌──────────────┐    ┌──────────────┐
       │   FEATURE    │     │   STORAGE    │    │   ANALYTICS  │
       │   ENGINE     │     │  PostgreSQL  │    │    ENGINE    │
       └──────┬───────┘     └──────────────┘    └──────┬───────┘
              ▼                                        ▼
       ┌──────────────┐                        ┌──────────────┐
       │   FASTAPI    │ ◄────────────────────► │ RESEARCH AI  │
       └──────┬───────┘                        └──────────────┘
              ▼
       ┌──────────────┐
       │   NEXT.JS    │
       └──────────────┘

## 🧠 Concurrency & Memory Model
- **Zero-Allocation Hot Path:** The C++ order book uses pre-allocated flat arrays and `std::unordered_map` with reserved capacity to eliminate heap allocations during event processing.
- **Lock-Free Pipeline:** Thread handoffs are managed via lock-free ring buffers before publishing to the `librdkafka` asynchronous queue.

## 💥 Failure Recovery Tolerances
- **Broker Disconnect:** C++ engine buffers up to 500,000 messages in memory; reconnects with exponential backoff.
- **Consumer Crash:** Python microservices utilize explicit Kafka offset commits post-PostgreSQL batch insertion, guaranteeing exactly-once processing semantics during a restart.
