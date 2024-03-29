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
- Сформировать таблицу с колонками: item_id, order_price, sale_price, date_added
- Создать код в Python для сравнения скоростей выполнения двух наших сценариев (брать средние значения результатов, чтобы исключить выбросы и получить объективное сравнение), вот подробные сценарии тестов:
    1) Оценить, как меняется скорость записи по мере заполнения таблицы, при каждом добавлении 50к строк
    2) Оценить, как быстро он может запихивать эти 50к строк (это не нужно для проектной задачи, но интересно)
    3) На сколько быстро я могу получать данные для каждого уникального предмета, при полном заполнении таблицы таких возвращаемых строк для каждого уникального id должно быть примерно 5к, а уникальных предметов примерно 100к (получить предельную скорость получения для каждой БД)
    4) Сравнить эту скорость при разном заполнении таблицы, для 1кк строк, 100кк и предельном в 500кк строк
    5) Отрисовать графики скоростей в matplotlib и агрегировать информацию о результатах в файл
</details>

---

<details>
  <summary>как запустить тест:</summary>

- создаем образ для тестируемой БД и запускаем контейнер (инструкции в комментариях в Dockerfil'ах)
- переходим в раздел с БД и запускаем код (для timescaleDB один файл, для mongoDB два разных (чтение и запись))
  
</details>

>
---
>

<details>
  <summary style="font-weight: bold;">Результаты тестов (от лучшего к худшему):</summary>
  
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

  <ul>
    <li>
      <details>
        <summary>Результат для postgres (одна таблица, указан index для item_id):</summary>
        1) скорость вставки в зависимости от размера таблицы (минимальный размер - 2.5кк, максимальный - 450кк)
        <ul>450кк строк</ul>
        <img src="postgres_simple\results_postgres_with_index_on_item_id\time_to_insert_at_size_450kk_rows.png">
        >> По итогу скорость добавления практически никак не менялась от 2кк до 500кк строк.
        <p> </p>
        2) скорсть получения всех строк по уникальному item_id в зависимости от размера таблицы (минимальный размер - 5кк, максимальный - 450кк). Уникальных item_id 100к, на каждый при максимальной загруженности приходится ~5к строк.
        <ul>5кк строк</ul>
        <img src="postgres_simple\results_postgres_with_index_on_item_id\time_to_select_data_for_unique_id_table_size_was_5kk_rows.png">
        <ul>50кк строк</ul>
        <img src="postgres_simple\results_postgres_with_index_on_item_id\time_to_select_data_for_unique_id_table_size_was_50kk_rows.png">
        <ul>250кк строк</ul>
        <img src="postgres_simple\results_postgres_with_index_on_item_id\time_to_select_data_for_unique_id_table_size_was_250kk_rows.png">
        <ul>450кк строк</ul>
        <img src="postgres_simple\results_postgres_with_index_on_item_id\time_to_select_data_for_unique_id_table_size_was_450kk_rows.png">
        >> Тут уже четко видна зависимость количества строк в таблице и среднего времени для ответа на запрос (от 0.002сек. при 2.5кк строк до 1.2сек. при 450кк строк)
      </details>
    </li>
  </ul>
  
  <ul>
    <li>
      <details>
        <summary>Результат для mongoDB:</summary>
        1) Средняя скорость для добавления 50к строк была примерно 0.3 секунды и не менялась от 3кк строк до 500кк строк (примерно схожие результаты у postgres)
        <p></p>
        2) Средняя скорость получения всех строк по уникальному item_id в зависимости от размера таблицы составила примерно 20 секунд и увеличивалась по мере роста числа записей в БД (минимальный размер - 2.5кк, максимальный - 500кк).
        <p></p>
        P.S. Именно поэтому я и не стал запариваться с картинками и описанием, так как результат для чтения слишком плачевный (в 10 раз медленнее чем у postgres), хуже работал только postgres без явной индексации по item_id
      </details>
    </li>
  </ul>
</details>


 ## Вывод:
 > Самым эффективным способом для чтения оказалось разделение данных на равные по размеру таблицы, разделение на 4 таблицы сократило время на получение всей информации для одного item_id в 2 раза (с 1.2 при одной таблице, до 0.55 при 4 таблицах), разделение на 10 таблиц дало прирост в скорости почти в 4 раза по сравнению с 1 таблицей.