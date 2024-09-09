## В данном репозитории я планирую сравнить postgres, timescaleDB и mongoDB для чтения и записи


<details>
  <summary>два основных сценария для теста:</summary>

>эти сценарии и есть моя основная нагрузка и сложность внутри реального проекта, для решения и были написаны эти тесты:
>1) запись 50к строк, вплоть до 500кк строк 
>2) так как в таблице будет примерно 100к уникальных id, указывающих на имена предметов, то на 1 предмет будет приходится примерно 5к записей, тут я и хочу проверить, на сколько шустро я буду получать эти 5к записей для каждого предмета, по мере заполнения таблицы
</details>

---

<details>
<summary>порядок проведения теста:</summary>

- Создать контейнер в Docker для каждой базы данных
- Запустить код, в этой ветке мы получаем и оцениваем среднее время для получения информации для случайного item_id, так как толькоэта метрика сейчас и важна (время добавление мы получаем, но впроде используется добавление по одному значениюв каждый список, тут мы сразу добавляем сформированные списки нужной длины, поэтому оценит ьобъективн овремя добавления мы не можем)
    
</details>

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


 ## Вывод:
 > Самым эффективным способом для чтения оказалось разделение данных на равные по размеру таблицы, разделение на 4 таблицы сократило время на получение всей информации для одного item_id в 2 раза (с 1.2 при одной таблице, до 0.55 при 4 таблицах), разделение на 10 таблиц дало прирост в скорости почти в 4 раза по сравнению с 1 таблицей.