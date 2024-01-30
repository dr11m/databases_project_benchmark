// Файл init.js для MongoDB
// Файл init.js в корне репозитория

db.createCollection("items");

// Создание индекса для поля item_id
db.items.createIndex({ "item_id": 1 }, { unique: true });