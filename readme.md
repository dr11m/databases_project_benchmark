
> В этой ветке мы получаем и оцениваем среднее время получения информации для случайного item_id, так как только эта метрика сейчас и важна (время добавление мы получаем, но в проде используется добавление по одному значению в каждый список, тут мы сразу добавляем сформированные списки нужной длины, поэтому оценить объективно время добавления мы не можем)

---

<details>
  <summary>как запустить тест:</summary>

- создаем образ для тестируемой БД и запускаем контейнер (инструкции в комментариях в Dockerfil'ах)

- pipenv install (можно с --ignore-pipfile)

- внутри файла с тестом (.py) есть конфиг, это и есть тестовые условия, которые можно менять
- запустить .py код
  
</details>

>
---
>

<details>
  <summary style="font-weight: bold;">Результаты тестов для разного кол-ва уникальных записей в БД (item_id) и разной длины списков для каждого уникального item_id:</summary>
  
  <ul>
    <li>
      <details>
        <summary>latest postgres:16.1, 1 таблица, 17к строк:</summary>
        <img src="postgres_simple_1_table\results\select_performance_plot_for_17k_unique_rows.png">
      </details>
    </li>
  </ul>
  
  <ul>
    <li>
      <details>
        <summary>latest postgres:16.1, 1 таблица, 50к строк:</summary>
        <img src="postgres_simple_1_table\results\select_performance_plot_for_50k_unique_rows.png">
      </details>
    </li>
  </ul>
  
</details>


 ## Вывод:
 > Получилось так, что при бльших объемах время на получение случайного item_id даже меньше (это скорее объясняется исправлениями кода и оптимизацией докера, который в процессе отвалился), я уверен, что если сейчас провести этот же тест для 17к и 50к строк, то мы получим минимальную разницу в пользу 17к. 
> Среднее время на получение крайне низкое, даже при значительном увеличение кол-ва строк. По сути это означает, что лимитов для меня нет, так в проде мой предел 30к строк и 4к для каждого списка.