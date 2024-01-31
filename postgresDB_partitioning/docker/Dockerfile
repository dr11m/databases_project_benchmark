# Dockerfile для TimescaleDB
# Файл Dockerfile в корне репозитория

# Базовый образ
FROM timescale/timescaledb:latest-pg12

# Копирование исходных файлов (для инициализации таблицы)
COPY init.sql /docker-entrypoint-initdb.d/


# создание образа и контейнера:
#  docker build -t timescaledb .
#  docker run --name timescaledb_container_partitioning -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres timescaledb
