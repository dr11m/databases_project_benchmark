from pymongo import MongoClient
import time
import matplotlib.pyplot as plt
import random


# Функция для подключения к MongoDB
def connect_mongodb():
    client = MongoClient('localhost', 27017)
    db = client['test_database']  # Замените 'your_database' на имя вашей базы данных
    return db

# Функция для получения количества записей в коллекции
def get_total_records(db):
    total_records = db.items.count_documents({})
    return total_records

# Функция для проведения теста чтения данных по уникальным id
def read_unique_id_test(amount_of_requests, db):
    times = []
    for _ in range(amount_of_requests):
        unique_id = random.randint(0, 49999)  # Случайный выбор уникального id
        start_time = time.time()
        cursor = db.items.find({"item_id": unique_id})
        rows = list(cursor)
        end_time = time.time()
        if _ % 10 == 0:
            times.append(end_time - start_time)
            print(end_time - start_time, _, amount_of_requests)
    return times

# Функция для отображения графика скорости теста
def plot_read_unique_id_test(times):
    plt.plot(range(len(times)), times, marker='o', linestyle='-', color='b')
    plt.xlabel("Query Number")
    plt.ylabel("Time (seconds)")
    plt.title("Read Speed Test for Unique IDs")
    plt.grid(True)
    plt.show()

# Основная функция для проведения теста
def main():
    db = connect_mongodb()

    amount_of_requests = 400  # Количество запросов

    # Тестирование скорости чтения по уникальным id
    times = read_unique_id_test(amount_of_requests, db)
    print("Average time per query:", sum(times) / len(times))

    plot_read_unique_id_test(times)


if __name__ == "__main__":
    main()
