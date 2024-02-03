-- Файл init.sql для TimescaleDB
-- Файл init.sql в корне репозитория

-- создаем 4 одинаковые таблицы

CREATE TABLE IF NOT EXISTS items_1 (
    item_id SERIAL,
    order_price FLOAT,
    sale_price FLOAT,
    date_added TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_item_id_1 ON items_1(item_id);

CREATE TABLE IF NOT EXISTS items_2 (
    item_id SERIAL,
    order_price FLOAT,
    sale_price FLOAT,
    date_added TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_item_id_2 ON items_2(item_id);

CREATE TABLE IF NOT EXISTS items_3 (
    item_id SERIAL,
    order_price FLOAT,
    sale_price FLOAT,
    date_added TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_item_id_3 ON items_3(item_id);

CREATE TABLE IF NOT EXISTS items_4 (
    item_id SERIAL,
    order_price FLOAT,
    sale_price FLOAT,
    date_added TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_item_id_4 ON items_4(item_id);
