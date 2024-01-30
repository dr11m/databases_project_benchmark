# Dockerfile для MongoDB
# Файл Dockerfile в корне репозитория

# Базовый образ
FROM mongo:latest

# Копирование исходных файлов инициализация таблицы
COPY init.js /docker-entrypoint-initdb.d/


# docker build -t mongodb .
# docker run -d --name mongodb_container -p 27017:27017 mongodb
