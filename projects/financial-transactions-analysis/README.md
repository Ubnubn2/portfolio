# анализ данных и разработка поисковика

Этот репозиторий содержит решения двух заданий:

1. **Анализ финансовых транзакций и клиентов** (папка `task1_analysis/`).
2. **Разработка краулера документов с полнотекстовым поиском** (папка `task2_crawler/`).

Оба проекта выполнены на Python и сопровождаются необходимой документацией, кодом и инструкциями по запуску.

---

## Структура репозитория

```.
├── .gitignore
├── README.md
├── task1_analysis/           # Первое задание
│   ├── README.md
│   ├── requirements.txt
│   ├── notebooks/             # Jupyter ноутбуки с анализом
│   └── src/                    # Вспомогательные скрипты 
├── task2_crawler/             # Второе задание
│   ├── README.md
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── scripts/                # Скрипты для генерации, краулинга и загрузки
│   └── data/                    # Временные данные 
└── docs/                        # Дополнительная документация 
```

---

## Задание 1. Анализ финансовых транзакций и клиентов

### Описание
Проведён полный анализ данных из файлов `transactions_data.xlsx` и `clients_data.json`:
- Очистка и предобработка (обработка пропусков, аномалий, приведение типов).
- Расчёт ключевых метрик: топ-5 услуг, средняя сумма по городам, услуга с наибольшей выручкой, распределение способов оплаты, выручка за последний месяц.
- Объединение с клиентскими данными, создание категорий капитала, анализ выручки по уровням.
- Визуализация результатов (гистограммы, столбчатые диаграммы, круговые диаграммы, график зависимости от возраста).
- Прогнозирование количества транзакций на следующий месяц с помощью линейной регрессии.

### Технологии
- Python 3.11
- pandas, numpy, matplotlib, seaborn
- scikit-learn
- Jupyter Notebook

### Как запустить
1. Установите зависимости:
   ```bash
   pip install -r task1_analysis/requirements.txt
   ```
2. Запустите Jupyter Notebook:
   ```bash
   jupyter notebook task1_analysis/notebooks/
   ```
3. Откройте файл `main.ipynb` и выполните все ячейки последовательно.  
   *Примечание:* файлы `transactions_data.xlsx` и `clients_data.json` должны лежать в той же папке, что и ноутбук (или пути в коде должны быть скорректированы).

---

## Задание 2. Краулер документов и полнотекстовый поиск

### Описание
Разработана система для сканирования хранилища файлов, извлечения текстовой информации и загрузки в PostgreSQL с полнотекстовым поиском.  
Функциональность:
- Генерация тестовых файлов (txt, docx, xlsx, pdf, а также архивы zip, rar, 7z).
- Рекурсивный краулинг папки `test_storage`, распаковка архивов, парсинг содержимого.
- Сохранение результатов в CSV.
- Загрузка CSV в PostgreSQL, создание GIN-индекса для полнотекстового поиска (tsvector).
- Примеры поисковых запросов с ранжированием результатов.

### Технологии
- Python 3.11
- Библиотеки: faker, python-docx, openpyxl, fpdf2, rarfile, py7zr, pandas, pdfplumber, psycopg2-binary
- PostgreSQL 15 (в Docker)
- Docker, Docker Compose

### Как запустить

1. Убедитесь, что установлены Docker и Docker Compose.
2. Перейдите в папку задания:
   ```bash
   cd task2_crawler
   ```
3. Запустите контейнеры:
   ```bash
   docker-compose up -d
   ```
4. Сгенерируйте тестовые файлы:
   ```bash
   docker-compose run --rm app python scripts/generate_files.py
   ```
5. Запустите краулер (извлечение текста в CSV):
   ```bash
   docker-compose run --rm app python scripts/crawler.py
   ```
6. Загрузите данные в PostgreSQL:
   ```bash
   docker-compose run --rm app python scripts/load_to_db.py
   ```
7. Проверьте поиск (пример в скрипте или через `psql`):
   ```bash
   docker exec -it postgres-fts psql -U postgres -d search_db -c "SELECT file_path, ts_headline('russian', content, plainto_tsquery('russian', 'John')) FROM files WHERE content_tsv @@ plainto_tsquery('russian', 'John');"
   ```

Результаты сохраняются в `data/crawled_data.csv`, а база данных — в томе Docker `postgres_data`.

---

## Требования к системе
- Python 3.8 или выше (для первого задания).
- Docker и Docker Compose (для второго задания).
- Для работы с RAR-архивами необходима утилита `unrar` (доступная в системе).

---

## Автор
Выполнила: Леонтьева Анна Владимировна  
Контакт-TG: @LEONTANNA
