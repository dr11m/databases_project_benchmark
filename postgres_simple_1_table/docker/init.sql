-- Файл init.sql для TimescaleDB
-- Файл init.sql в корне репозитория

CREATE TABLE IF NOT EXISTS items (
    item_id SERIAL,
    order_price FLOAT,
    sale_price FLOAT,
    date_added TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_item_id ON items(item_id);
