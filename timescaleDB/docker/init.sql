-- Файл init.sql для TimescaleDB
-- Файл init.sql в корне репозитория

CREATE TABLE IF NOT EXISTS items (
    item_id SERIAL,
    order_price FLOAT,
    sale_price FLOAT,
    date_added TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

SELECT create_hypertable('items', 'date_added');


-- docs: https://docs.timescale.com/tutorials/latest/blockchain-query/blockchain-dataset/
