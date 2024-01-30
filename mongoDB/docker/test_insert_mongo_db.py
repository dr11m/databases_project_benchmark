from pymongo import MongoClient
import time
import matplotlib.pyplot as plt
import random


# Функция для получения количества записей в коллекции
def get_total_records(db):
    total_records = db.items.count_documents({})
    return total_records

# Функция для записи данных в MongoDB
def write_to_mongodb(db, data):
    result = db.items.insert_many(data)

def generate_random_prices(size):
    return [{"item_id": i, "order_price": random.uniform(1.0, 100.0), "sale_price": random.uniform(1.0, 100.0)} for i in range(size)]

# Функция для проведения теста записи данных
def write_speed_test(insert_iters, insert_size_batch, db):
    times = []
    for i in range(insert_iters):
        data = generate_random_prices(insert_size_batch)
        start_time = time.time()
        write_to_mongodb(db, data)
        end_time = time.time()
        if i % 10 == 0:
            print(end_time - start_time)
            times.append(end_time - start_time)
    return times

# Функция для отображения графика скорости теста
def plot_speed_test(times, test_type):
    plt.plot(range(len(times)), times)
    plt.xlabel("Iteration")
    plt.ylabel("Time (seconds)")
    plt.title(f"{test_type} Speed Test for MongoDB")
    plt.grid(True)
    plt.show()

# Основная функция для проведения теста
def main():
    client = MongoClient('localhost', 27017)
    db = client['test_database']  # Замените 'your_database' на имя вашей базы данных

    total_records = get_total_records(db)
    print(f"Total records in the collection: {total_records}")


    db.items.delete_many({})

    total_records = get_total_records(db)
    print(f"Total records in the collection: {total_records}")


    insert_size_batch = 50000
    insert_iters = 100

    # Тестирование скорости записи
    times = write_speed_test(insert_iters, insert_size_batch, db)
    plot_speed_test(times, "Write")

    total_records = get_total_records(db)
    print(f"Total records in the collection: {total_records}")


if __name__ == "__main__":
    main()
