import psycopg2
from psycopg2 import pool
import time
import matplotlib.pyplot as plt
import io
import random


# Функция для подключения к TimescaleDB с использованием пула подключений
def connect_timescaledb():
    conn_pool = pool.SimpleConnectionPool(
        1,  # Минимальное количество соединений
        10,  # Максимальное количество соединений
        host="localhost",
        database="postgres",
        user="postgres",
        password="postgres",
        port="5432"
    )
    return conn_pool

# Функция для получения количества записей в таблице
def get_total_records():
    conn_pool = connect_timescaledb()
    conn = conn_pool.getconn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM items")
    total_records = cur.fetchone()[0]
    conn_pool.putconn(conn)
    conn_pool.closeall()
    return total_records

# Функция для записи данных в TimescaleDB с использованием COPY
def write_to_timescaledb(conn_pool, data):
    conn = conn_pool.getconn()
    cur = conn.cursor()
    buffer = io.StringIO()
    for row in data:
        buffer.write('\t'.join(map(str, row)) + '\n')
    buffer.seek(0)
    cur.copy_from(buffer, 'items', columns=('item_id', 'order_price', 'sale_price'))
    conn.commit()
    cur.close()
    conn_pool.putconn(conn)

def generate_random_prices(size):
    return [(random.uniform(1.0, 100.0), random.uniform(1.0, 100.0)) for _ in range(size)]

# Функция для проведения теста записи данных
def write_speed_test(insert_iters, insert_size_batch):
    times = []
    conn_pool = connect_timescaledb()
    for i in range(insert_iters):
        data = [(j, *prices) for j, prices in enumerate(generate_random_prices(insert_size_batch))]
        start_time = time.time()
        write_to_timescaledb(conn_pool, data)
        end_time = time.time()
        if i % 10 == 0:
            times.append(end_time - start_time)
    conn_pool.closeall()
    return times

# Функция для отображения графика скорости теста
def plot_speed_test(times, data_sizes, test_type):
    plt.plot([i+1 for i in range(len(times))], times)
    plt.xlabel("Iteration")
    plt.ylabel("Time (seconds)")
    plt.title(f"{test_type} Speed Test for TimescaleDB")
    plt.grid(True)
    plt.show()

# Основная функция для проведения теста
def main():
    total_records = get_total_records()
    print(f"Total records in the table: {total_records}")

    insert_size_batch = 50000
    insert_iters = 10000

    # Тестирование скорости записи
    times = write_speed_test(insert_iters, insert_size_batch)
    plot_speed_test(times, range(1, insert_iters + 1), "Write")

    total_records = get_total_records()
    print(f"Total records in the table: {total_records}")

if __name__ == "__main__":
    main()
