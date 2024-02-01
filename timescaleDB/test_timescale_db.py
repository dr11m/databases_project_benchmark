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

def clear_table(conn_pool):
    conn = conn_pool.getconn()
    cur = conn.cursor()
    print("clearing the table...")
    cur.execute("DELETE FROM items")
    conn.commit()
    print("table was cleared")
    conn_pool.putconn(conn)

def get_total_records(conn_pool):
    conn = conn_pool.getconn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM items")
    total_records = cur.fetchone()[0]
    cur.close()  # Закройте только соединение после использования, не весь пул соединений
    conn_pool.putconn(conn)
    return total_records

# Функция для проведения теста чтения данных по уникальным id
def read_unique_id_test(amount_of_requests, conn_pool):
    times = []
    conn = conn_pool.getconn()
    cur = conn.cursor()
    for i in range(amount_of_requests):
        unique_id = random.randint(0, 49999)  # Случайный выбор уникального id
        start_time = time.time()
        cur.execute("SELECT * FROM items WHERE item_id = %s", (unique_id,))
        #cur.execute("SELECT * FROM items WHERE item_id = %s ORDER BY date_added ASC", (unique_id,))
        rows = cur.fetchall()
        end_time = time.time()
        times.append(end_time - start_time)
        print(f"insert: {i}/{amount_of_requests} -- {end_time - start_time}")
    cur.close()
    conn_pool.putconn(conn)
    return times

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
def write_speed_test(config, iteration_amount, conn_pool):
    times = []
    for i in range(iteration_amount):
        data = [(j, *prices) for j, prices in enumerate(generate_random_prices(config["rows_to_insert_at_a_time"]))]
        start_time = time.time()
        write_to_timescaledb(conn_pool, data)
        end_time = time.time()
        if i % 10 == 0:
            times.append(end_time - start_time)
            print(f"insert: {i}/{iteration_amount} -- {end_time - start_time}")
    return times

def save_plot_test_result_insert(times, conn_pool):
    plt.clf()
    plt.figure(figsize=(15, 7))
    plt.plot(range(len(times)), times, marker='o', linestyle='-', color='b')
    plt.xlabel("rows_amount = iter * 50k rows")
    plt.ylabel("Time (seconds)")
    total_records = get_total_records(conn_pool)
    plt.title(f"avg time in seconds for adding 50k rows, max table size at the end is {int(total_records / 1000000)}kk rows")
    plt.grid(True)
    plt.savefig(f"timescaleDB/results/time_to_insert_at_size_{int(total_records / 1000000)}kk_rows.png")  # Сохранить график в файл

def save_plot_test_result_select(times, conn_pool):
    plt.clf()
    plt.figure(figsize=(15, 7))
    plt.plot(range(len(times)), times, marker='o', linestyle='-', color='b')
    plt.xlabel("Iterations")
    plt.ylabel("Time (seconds)")
    total_records = get_total_records(conn_pool)
    plt.title(f"avg time in seconds to get data for unique item_id ~(table_size / 100k), table size was {int(total_records / 1000000)}kk rows")
    plt.grid(True)
    plt.savefig(f"timescaleDB/results/time_to_select_data_for_unique_id_table_size_was_{int(total_records / 1000000)}kk_rows.png")  # Сохранить график в файл


def run_test_scenario(conn_pool):
    config = {
            "rows_to_insert_at_a_time": 50000,
            "unique_amount": 100000,
            "iterations_at_each_stage": [100, 900, 4000],  # 50000 * 100 + 50000 * 1000
            "iterations_to_get_mean_time_of_select": 30
        }
    
    for iteration_amount in config["iterations_at_each_stage"]:
        times = write_speed_test(config, iteration_amount, conn_pool)
        save_plot_test_result_insert(times, conn_pool)
        
        times = read_unique_id_test(config["iterations_to_get_mean_time_of_select"], conn_pool)
        save_plot_test_result_select(times, conn_pool)
# Основная функция для проведения теста
def main():
    conn_pool = connect_timescaledb()

    #clear_table(conn_pool)

    total_records = get_total_records(conn_pool)
    print(f"Total records in the table: {int(total_records / 1000000)}kk")

    run_test_scenario(conn_pool)

    # Закрыть пул соединений после завершения всех операций
    conn_pool.closeall()

if __name__ == "__main__":
    main()
