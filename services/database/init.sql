CREATE TABLE IF NOT EXISTS market_events (
    id BIGSERIAL PRIMARY KEY,
    timestamp_ns BIGINT NOT NULL,
    symbol VARCHAR(16) NOT NULL,
    best_bid DOUBLE PRECISION,
    best_ask DOUBLE PRECISION,
    spread DOUBLE PRECISION,
    mid_price DOUBLE PRECISION,
    imbalance DOUBLE PRECISION,
    latency_ns BIGINT
);

CREATE TABLE IF NOT EXISTS market_features (
    id BIGSERIAL PRIMARY KEY,
    timestamp_ns BIGINT NOT NULL,
    symbol VARCHAR(16) NOT NULL,
    vwap DOUBLE PRECISION,
    ema_20 DOUBLE PRECISION,
    volatility DOUBLE PRECISION,
    momentum DOUBLE PRECISION
);

CREATE INDEX idx_market_events_symbol_time ON market_events(symbol, timestamp_ns DESC);
CREATE INDEX idx_market_features_symbol_time ON market_features(symbol, timestamp_ns DESC);
