
> В этой ветке мы получаем и оцениваем среднее время получения информации для случайного item_id, так как только эта метрика сейчас и важна (время добавление мы получаем, но в проде используется добавление по одному значению в каждый список, тут мы сразу добавляем сформированные списки нужной длины, поэтому оценить объективно время добавления мы не можем)

---

<details>
  <summary>как запустить тест:</summary>
- создаем образ для тестируемой БД и запускаем контейнер (инструкции в комментариях в Dockerfil'ах)
- pipenv install (можно с --ignore-pipfile)
- запустить .py код
  
</details>

>
---
>

<details>
  <summary style="font-weight: bold;">Результаты тестов для разного кол-ва уникальных записей в БД (item_id) и разной длины списков для каждого уникального item_id: >Нужно получить результаты, а потом обновить даныне ниже< </summary>
  
  <ul>
    <li>
      <details>
        <summary>latest postgres:16.1 (данные равномерно распределены в 10 таблиц):</summary>
        1) среднее время записи 50к строк при размере таблиц в 500кк записей (равномерно распределены в 10 таблицах)
        <img src="postgresDB_partitioning_into_10_tables\results_latest_postgres\time_to_insert_at_size_500kk_rows.png">
        2) скорость чтения в зависимости от размера (от 5кк до 500кк), для получения информации для одного item_id делается 10 параллельных запросов в 10 таблиц
        <p> </p>
        <ul>5кк строк</ul>
        <img
        src="postgresDB_partitioning_into_10_tables\results_latest_postgres\time_to_select_data_for_unique_id_table_size_was_5kk_rows.png">
        <ul>50кк строк</ul>
        <img
        src="postgresDB_partitioning_into_10_tables\results_latest_postgres\time_to_select_data_for_unique_id_table_size_was_50kk_rows.png">
        <ul>250кк строк</ul>
        <img
        src="postgresDB_partitioning_into_10_tables\results_latest_postgres\time_to_select_data_for_unique_id_table_size_was_250kk_rows.png">
        <ul>500кк строк</ul>
        <img
        src="postgresDB_partitioning_into_10_tables\results_latest_postgres\time_to_select_data_for_unique_id_table_size_was_500kk_rows.png">
      </details>
    </li>
  </ul>
  
  <ul>
    <li>
      <details>
        <summary>latest postgres:16.1 (данные равномерно распределены в 4 таблицы):</summary>
        1) среднее время записи 50к строк при размере таблиц в 500кк записей (равномерно в 4 таблицах)
        <img src="postgresDB_partitioning_into_4_tables\results_latest_postgres\time_to_insert_at_size_500kk_rows.png">
        2) скорость чтения в зависимости от размера (от 5кк до 500кк), для получения информации для одного item_id делается 4 параллельных запроса в 4 таблицы
        <p> </p>
        <ul>5кк строк</ul>
        <img
        src="postgresDB_partitioning_into_4_tables\results_latest_postgres\time_to_select_data_for_unique_id_table_size_was_5kk_rows.png">
        <ul>50кк строк</ul>
        <img
        src="postgresDB_partitioning_into_4_tables\results_latest_postgres\time_to_select_data_for_unique_id_table_size_was_50kk_rows.png">
        <ul>250кк строк</ul>
        <img
        src="postgresDB_partitioning_into_4_tables\results_latest_postgres\time_to_select_data_for_unique_id_table_size_was_250kk_rows.png">
        <ul>500кк строк</ul>
        <img
        src="postgresDB_partitioning_into_4_tables\results_latest_postgres\time_to_select_data_for_unique_id_table_size_was_500kk_rows.png">
      </details>
    </li>
  </ul>
  
</details>


 ## Вывод (ОБНОВИТЬ):
 > ...