# Dockerfile для MongoDB
# Файл Dockerfile в корне репозитория

# Базовый образ
FROM mongo:latest

# Копирование исходных файлов инициализация таблицы
COPY init.js /docker-entrypoint-initdb.d/
