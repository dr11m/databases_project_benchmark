import psycopg2
from psycopg2 import pool
import time
import matplotlib.pyplot as plt
import io
import random
import threading


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

def clear_tables(conn_pool):
    conn = conn_pool.getconn()
    cur = conn.cursor()
    print("clearing the tables...")
    cur.execute("DELETE FROM items_1")
    cur.execute("DELETE FROM items_2")
    cur.execute("DELETE FROM items_3")
    cur.execute("DELETE FROM items_4")
    conn.commit()
    print("tables were cleared")
    conn_pool.putconn(conn)

def get_total_records(conn_pool):
    conn = conn_pool.getconn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM items_1")
    total_records = cur.fetchone()[0]
    cur.close()  
    conn_pool.putconn(conn)
    return total_records

def read_from_table(cur, table_name, unique_id, all_results, conn, conn_pool):
    cur.execute(f"SELECT * FROM {table_name} WHERE item_id = %s", (unique_id,))
    rows = cur.fetchall()
    all_results.extend(rows)  # Add results from the table to the overall results
    conn_pool.putconn(conn)  # Return the connection to the pool

def read_unique_id_test(amount_of_requests, conn_pool):
    times = []
    for i in range(amount_of_requests):
        all_results = []  # List to store results from all tables
        unique_id = random.randint(0, 49999)  # Randomly choose a unique id
        start_time = time.time()

        threads = []
        for table_num in range(1, 5):
            conn = conn_pool.getconn()  # Get a new connection for each thread
            cur = conn.cursor()
            thread = threading.Thread(target=read_from_table, args=(cur, f"items_{table_num}", unique_id, all_results, conn, conn_pool))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()  # Wait for all threads to finish

        end_time = time.time()
        times.append(end_time - start_time)
        print(f"insert: {i}/{amount_of_requests} -- {end_time - start_time}, len {len(all_results)}")

    return times



# Функция для записи данных в TimescaleDB с использованием COPY
def write_to_timescaledb(conn_pool, data, i):
    conn = conn_pool.getconn()
    cur = conn.cursor()
    buffer = io.StringIO()
    for row in data:
        buffer.write('\t'.join(map(str, row)) + '\n')
    buffer.seek(0)
    cur.copy_from(buffer, f'items_{i}', columns=('item_id', 'order_price', 'sale_price'))
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
        if i % 4 == 0:
            write_to_timescaledb(conn_pool, data, 1)
        elif i % 4 == 1:
            write_to_timescaledb(conn_pool, data, 2)
        elif i % 4 == 2:
            write_to_timescaledb(conn_pool, data, 3)
        else:
            write_to_timescaledb(conn_pool, data, 4)
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
    plt.savefig(f"postgresDB_partitioning/results_latest_postgres/time_to_insert_at_size_{int(total_records / 1000000)}kk_rows.png")  # Сохранить график в файл

def save_plot_test_result_select(times, conn_pool):
    plt.clf()
    plt.figure(figsize=(15, 7))
    plt.plot(range(len(times)), times, marker='o', linestyle='-', color='b')
    plt.xlabel("Iterations")
    plt.ylabel("Time (seconds)")
    total_records = get_total_records(conn_pool)
    plt.title(f"avg time in seconds to get data for unique item_id ~(table_size / 100k), table size was {int(total_records / 1000000)}kk rows")
    plt.grid(True)
    plt.savefig(f"postgresDB_partitioning/results_latest_postgres/time_to_select_data_for_unique_id_table_size_was_{int(total_records / 1000000)}kk_rows.png")  # Сохранить график в файл


def run_test_scenario(conn_pool):
    config = {
            "rows_to_insert_at_a_time": 50000,
            "unique_amount": 100000,
            "iterations_at_each_stage": [100, 900, 4000, 5000],  # 50000 * 100 + 50000 * 1000
            "iterations_to_get_mean_time_of_select": 50
        }
    
    for iteration_amount in config["iterations_at_each_stage"]:
        times = write_speed_test(config, iteration_amount, conn_pool)
        save_plot_test_result_insert(times, conn_pool)
        
        times = read_unique_id_test(config["iterations_to_get_mean_time_of_select"], conn_pool)
        save_plot_test_result_select(times, conn_pool)


def main():
    conn_pool = connect_timescaledb()

    # clear_tables(conn_pool)

    total_records = get_total_records(conn_pool)
    print(f"Total records in the table: {total_records}")

    run_test_scenario(conn_pool)

    conn_pool.closeall()

if __name__ == "__main__":
    main()
