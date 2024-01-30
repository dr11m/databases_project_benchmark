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
def get_total_records(conn_pool):
    conn = conn_pool.getconn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM items")
    total_records = cur.fetchone()[0]
    conn.close()  # Закройте соединение после использования, а не весь пул соединений
    return total_records

def plot_read_unique_id_test(times):
    plt.plot(range(len(times)), times, marker='o', linestyle='-', color='b')
    plt.xlabel("Query Number")
    plt.ylabel("Time (seconds)")
    plt.title("Read Speed Test for Unique IDs")
    plt.grid(True)
    plt.show()

# Функция для проведения теста чтения данных по уникальным id
def read_unique_id_test(amount_of_requests, conn_pool):
    times = []
    conn = conn_pool.getconn()
    cur = conn.cursor()
    for _ in range(amount_of_requests):
        unique_id = random.randint(0, 49999)  # Случайный выбор уникального id
        start_time = time.time()
        cur.execute("SELECT * FROM items WHERE item_id = %s", (unique_id,))
        #cur.execute("SELECT * FROM items WHERE item_id = %s ORDER BY date_added ASC", (unique_id,))
        rows = cur.fetchall()
        end_time = time.time()
        if _ % 10 == 0:
            times.append(end_time - start_time)
            print(end_time - start_time, _, amount_of_requests)
    cur.close()
    conn_pool.putconn(conn)
    return times

# Основная функция для проведения теста
def main():
    conn_pool = connect_timescaledb()

    amount_of_requests = 400  # Количество запросов

    # Тестирование скорости чтения по уникальным id
    times = read_unique_id_test(amount_of_requests, conn_pool)
    print("Average time per query:", sum(times) / len(times))

    plot_read_unique_id_test(times)

    # Закройте пул соединений в конце работы программы
    conn_pool.closeall()

if __name__ == "__main__":
    conn_pool = connect_timescaledb()  # Установите соединение здесь
    #total_records = get_total_records(conn_pool)  # И передайте объект пула соединений
    #print(f"Total records in the table: {total_records}")
    main()
