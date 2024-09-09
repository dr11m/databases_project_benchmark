import os
from psycopg2 import pool
import time
import numpy as np
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
import random
from loguru import logger


table_name = "items_test"

config = {
    "unique_items": 50000,
    "list_lengths": [500, 5000, 10000, 25000],  # Длины списков для каждого этапа
    "iterations_to_get_mean_time_of_select": 10  # Число итераций для измерения времени SELECT
}

conn_pool = None

# Создание таблицы, если она не существует
def create_table_if_not_exists():
    with conn_pool.getconn() as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    item_id VARCHAR(255) PRIMARY KEY,
                    order_prices FLOAT[],
                    sale_prices FLOAT[],
                    dates_added BIGINT[]
                )
            """)
            conn.commit()
            logger.info(f"Table {table_name} created or already exists.")

# Инициализация пула соединений
def init_connection_pool():
    global conn_pool
    if not conn_pool:
        conn_pool = pool.SimpleConnectionPool(
            1,  # Минимальное количество соединений
            20,  # Максимальное количество соединений
            host="localhost",
            database="postgres",
            user="postgres",
            password="postgres",
            port="5432"
        )

# Очистка таблицы
def clear_table():
    with conn_pool.getconn() as conn:
        with conn.cursor() as cur:
            logger.info("Clearing the table...")
            cur.execute(f"DELETE FROM {table_name}")
            conn.commit()
            logger.info("Table was cleared")

# Получение общего количества записей
def get_total_records():
    with conn_pool.getconn() as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT COUNT(*) FROM {table_name}")
            total_records = cur.fetchone()[0]
            logger.info(f"Total records: {total_records}")
            return total_records

def parallel_write_to_db(chunk):
    with conn_pool.getconn() as conn:
        with conn.cursor() as cur:
            insert_query = f"""
                INSERT INTO {table_name} (item_id, order_prices, sale_prices, dates_added)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (item_id)
                DO UPDATE
                SET order_prices = {table_name}.order_prices || EXCLUDED.order_prices,
                    sale_prices = {table_name}.sale_prices || EXCLUDED.sale_prices,
                    dates_added = {table_name}.dates_added || EXCLUDED.dates_added
            """
            cur.executemany(insert_query, chunk)
            conn.commit()
    logger.info(f"Chunk of {len(chunk)} items processed.")

def write_to_db_parallel(data, num_workers=4):
    chunk_size = len(data) // num_workers
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    
    logger.info(f"Starting parallel write with {num_workers} workers.")
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = {executor.submit(parallel_write_to_db, chunk): chunk for chunk in chunks}
        for future in as_completed(futures):
            chunk = futures[future]
            try:
                future.result()
            except Exception as exc:
                logger.info(f'Generated an exception: {exc}')
            else:
                logger.info(f"Chunk processed successfully.")
    logger.info("Parallel write completed.")

# Измерение времени выборки
def measure_select_time():
    select_times = []
    for _ in range(config["iterations_to_get_mean_time_of_select"]):
        start_time = time.time()
        with conn_pool.getconn() as conn:
            with conn.cursor() as cur:
                # Выборка случайного элемента из БД
                cur.execute(f"SELECT * FROM {table_name} ORDER BY RANDOM() LIMIT 1")
                cur.fetchone()
        select_times.append(time.time() - start_time)
    
    mean_select_time = sum(select_times) / len(select_times)
    logger.info(f"Среднее время SELECT: {mean_select_time:.6f} секунд")
    return select_times, mean_select_time

def plot_insert_and_select_times(all_select_times):
    n = len(config["list_lengths"])
    rows = (n + 1) // 2  # Округление вверх для нечетного количества
    cols = 2 if n > 1 else 1

    fig, axs = plt.subplots(rows, cols, figsize=(15, 5 * rows))
    fig.suptitle("SELECT Performance for Different List Lengths")

    if n == 1:
        axs = np.array([[axs]])  # Преобразование в 2D массив для единообразия
    elif n == 2:
        axs = axs.reshape(1, -1)  # Преобразование в 2D массив для двух графиков

    for i, list_length in enumerate(config["list_lengths"]):
        row = i // 2
        col = i % 2
        
        ax = axs[row, col]
        ax.plot(range(1, len(all_select_times[i]) + 1), all_select_times[i], marker='o')
        ax.set_title(f"List Length: {list_length}")
        ax.set_xlabel("Iteration")
        ax.set_ylabel("SELECT Time (s)")
        ax.grid(True)

    # Удаление лишних подграфиков
    for i in range(n, rows * cols):
        fig.delaxes(axs.flatten()[i])

    plt.tight_layout()
    
    # Create a 'results' directory if it doesn't exist
    if not os.path.exists('results'):
        os.makedirs('results')
    
    # Save the plot as a PNG file
    plt.savefig(f'results/select_performance_plot_for_{config["unique_items"]}k_unique_rows.png')
    logger.info("Performance plot saved as 'results/performance_plot.png'")
    
    plt.show()

def run_test():
    init_connection_pool()
    create_table_if_not_exists()
    
    insert_times = []
    all_select_times = []

    base_timestamp = int(time.time())

    for list_length in config["list_lengths"]:
        clear_table()
        test_data = []
        for i in range(config["unique_items"]):
            order_prices = [random.random() * 100 for _ in range(list_length)]
            sale_prices = [random.random() * 100 for _ in range(list_length)]
            timestamps = [base_timestamp + j for j in range(list_length)]
            test_data.append((f"item_{i}", order_prices, sale_prices, timestamps))
        
        start_time = time.time()
        write_to_db_parallel(test_data)
        insert_time = time.time() - start_time
        insert_times.append(insert_time)

        total_records = get_total_records()
        logger.info(f"Total records after insert: {total_records}")
        logger.info(f"Time to insert {config['unique_items']} items with list length {list_length}: {insert_time:.2f} seconds")

        # Измерение времени SELECT после каждого этапа вставки
        select_times, mean_select_time = measure_select_time()
        all_select_times.append(select_times)
        logger.info(f"Average SELECT time for list length {list_length}: {mean_select_time:.6f} seconds")

        # Увеличиваем базовую временную метку для следующей итерации
        base_timestamp += list_length

    # Построение графиков
    plot_insert_and_select_times(all_select_times)

    # Вывод сводной информации
    logger.info("\nTest results summary:")
    for i, length in enumerate(config["list_lengths"]):
        logger.info(f"List length {length}:")
        logger.info(f"  Insert time: {insert_times[i]:.2f} seconds")
        logger.info(f"  Average SELECT time: {sum(all_select_times[i]) / len(all_select_times[i]):.6f} seconds")
        logger.info(f"  Min SELECT time: {min(all_select_times[i]):.6f} seconds")
        logger.info(f"  Max SELECT time: {max(all_select_times[i]):.6f} seconds")

if __name__ == "__main__":
    run_test()