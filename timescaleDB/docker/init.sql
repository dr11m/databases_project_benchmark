-- Файл init.sql для TimescaleDB
-- Файл init.sql в корне репозитория

CREATE TABLE IF NOT EXISTS items (
    item_id SERIAL,
    order_price FLOAT,
    sale_price FLOAT,
    date_added TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- TODO реализовать hypertable SELECT create_hypertable('transactions', by_range('time')); 
-- docs: https://docs.timescale.com/tutorials/latest/blockchain-query/blockchain-dataset/
