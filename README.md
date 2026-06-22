# 📊 Portfolio: Data Engineering & DevOps

**Анна Леонтьева** | Data Engineer / DevOps Engineer

- 🔗 GitHub: [@Ubnubn2](https://github.com/Ubnubn2)
- 📧 Email: anna.leonteva.2016@gmail.com
- 💬 Telegram: @LEONTANNA

---

## 📌 Краткий обзор

Специалист по разработке и оптимизации **ETL-процессов**, **хранилищ данных (DWH)** и **DevOps инфраструктуры**. Опыт работы с PostgreSQL, Python, Airflow, Docker. Ориентирована на масштабируемость, качество данных и автоматизацию.

**Ключевые компетенции:**
- ✅ SQL (SELECT, GROUP BY, Window Functions, JOINs, CTEs)
- ✅ Python (pandas, scikit-learn, data processing)
- ✅ ETL/ELT процессы и архитектура DWH
- ✅ Docker & Docker Compose
- ✅ Airflow (DAG разработка)
- ✅ Data Quality & Profiling
- ✅ CI/CD Pipeline (GitHub Actions)
- ✅ Bash scripting
- ✅ PostgreSQL, индексирование, оптимизация

---

## 🎯 Проекты

### 1️⃣ **Bookstore Analytics Platform** — Complete DWH Pipeline

**Описание:** Полный цикл ETL от исходных данных до аналитического дашборда. Демонстрирует работу с данными разных бизнес-областей, трансформацию и визуализацию.

**Стек:**
- 📦 Backend: PostgreSQL 15, Python 3.11
- 🔄 Data Processing: pandas, NumPy, scikit-learn
- 📊 Visualization: matplotlib, seaborn, Power BI
- 🐳 Infrastructure: Docker, Docker Compose

**Реализованный функционал:**

#### Extraction & Transformation:
```sql
-- Stage 1: Raw данные в staging таблицы
CREATE TABLE stg_books (
    book_id UUID PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author_id UUID NOT NULL,
    price DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Stage 2: Очистка и обогащение данных
SELECT 
    book_id,
    title,
    author_name,
    price,
    CASE 
        WHEN price < 100 THEN 'Budget'
        WHEN price < 500 THEN 'Standard'
        ELSE 'Premium'
    END as price_category,
    DENSE_RANK() OVER (ORDER BY price DESC) as price_rank
FROM stg_books
WHERE price IS NOT NULL;
```

#### Analytics Layer:
```sql
-- RFM-сегментация с Window Functions
WITH customer_metrics AS (
    SELECT 
        c.customer_id,
        MAX(o.order_date) as last_purchase_date,
        COUNT(DISTINCT o.order_id) as purchase_count,
        SUM(o.total_amount) as lifetime_value,
        NTILE(5) OVER (ORDER BY MAX(o.order_date) DESC) as recency_quintile,
        NTILE(5) OVER (ORDER BY COUNT(DISTINCT o.order_id) DESC) as frequency_quintile,
        NTILE(5) OVER (ORDER BY SUM(o.total_amount) DESC) as monetary_quintile
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id
)
SELECT 
    customer_id,
    last_purchase_date,
    purchase_count,
    lifetime_value,
    (recency_quintile || frequency_quintile || monetary_quintile)::INT as rfm_segment,
    CASE 
        WHEN recency_quintile >= 4 AND frequency_quintile >= 4 AND monetary_quintile >= 4 THEN 'Champions'
        WHEN recency_quintile >= 4 AND (frequency_quintile >= 3 OR monetary_quintile >= 3) THEN 'Loyal Customers'
        WHEN recency_quintile >= 3 THEN 'Potential Loyalist'
        ELSE 'At Risk'
    END as customer_segment
FROM customer_metrics
ORDER BY lifetime_value DESC;
```

**Результаты:**
- 📈 Топ-10 книг по выручке
- 👥 RFM-сегментация (5 групп с классификацией)
- 📊 Повторные покупки: 97.5%
- 🔮 Прогноз спроса: linear regression
- 📉 10+ визуализаций

**Запуск проекта:**

```bash
cd projects/bookstore-analytics

# 1. Развертывание БД
docker run --name bookstore-db \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -d -p 5432:5432 postgres:15

# 2. Подготовка окружения
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt

# 3. Инициализация БД и данных
python src/create_tables.py
python src/generate_data.py

# 4. Анализ
jupyter notebook stage3_analysis.ipynb

# 5. Cleanup
docker stop bookstore-db && docker rm bookstore-db
```

**GitHub:** [bookstore-analytics](./projects/bookstore-analytics/)

---

### 2️⃣ **Financial Transactions Analysis** — Data Quality & Profiling

**Описание:** Анализ 10,000+ финансовых записей с акцентом на качество данных, профилирование и валидацию.

**Стек:**
- 🐍 Python 3.11, pandas, scikit-learn
- 🗄️ PostgreSQL, GIN-индексы
- 🐳 Docker Compose
- 📋 Data Quality Framework

**Task 1: Очистка и анализ транзакций**

```python
# data_profiler.py - Профилирование данных (как в Ozon)
import pandas as pd
from typing import Dict

class DataProfiler:
    """
    Инструмент для профилирования данных
    Используется для анализа качества входящих данных
    """
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.profile = {}
    
    def profile_columns(self) -> Dict:
        """Профилирование каждой колонки"""
        for col in self.df.columns:
            self.profile[col] = {
                'data_type': str(self.df[col].dtype),
                'non_null_count': self.df[col].notna().sum(),
                'null_count': self.df[col].isna().sum(),
                'null_percentage': round(self.df[col].isna().sum() / len(self.df) * 100, 2),
                'unique_values': self.df[col].nunique(),
                'duplicates': self.df[col].duplicated().sum(),
            }
            
            # Числовые колонки
            if self.df[col].dtype in ['int64', 'float64']:
                self.profile[col].update({
                    'mean': self.df[col].mean(),
                    'median': self.df[col].median(),
                    'std': self.df[col].std(),
                    'min': self.df[col].min(),
                    'max': self.df[col].max(),
                    'q25': self.df[col].quantile(0.25),
                    'q75': self.df[col].quantile(0.75),
                })
        
        return self.profile
    
    def detect_anomalies(self, columns: list) -> Dict:
        """Обнаружение аномалий (IQR метод)"""
        anomalies = {}
        for col in columns:
            if self.df[col].dtype in ['int64', 'float64']:
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers = self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)]
                anomalies[col] = {
                    'outlier_count': len(outliers),
                    'outlier_percentage': round(len(outliers) / len(self.df) * 100, 2),
                    'bounds': {'lower': lower_bound, 'upper': upper_bound}
                }
        
        return anomalies

# Использование
df = pd.read_csv('transactions.csv')
profiler = DataProfiler(df)
profile = profiler.profile_columns()
anomalies = profiler.detect_anomalies(['amount', 'customer_age'])
print(profile)
print(anomalies)
```

```python
# data_quality_checks.py - Валидация качества данных
class DataQualityValidator:
    """
    Валидация данных на соответствие бизнес-требованиям
    """
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.validation_results = {}
    
    def check_null_ratios(self, thresholds: Dict[str, float]) -> Dict:
        """Проверка % NULL значений"""
        results = {}
        for col, threshold in thresholds.items():
            null_pct = self.df[col].isna().sum() / len(self.df) * 100
            status = "PASS" if null_pct <= threshold else "FAIL"
            results[col] = {
                'null_percentage': round(null_pct, 2),
                'threshold': threshold,
                'status': status
            }
        return results
    
    def check_duplicates(self, subset: list) -> Dict:
        """Проверка дубликатов"""
        duplicates = self.df.duplicated(subset=subset).sum()
        return {
            'duplicate_count': duplicates,
            'duplicate_percentage': round(duplicates / len(self.df) * 100, 2),
            'status': 'FAIL' if duplicates > 0 else 'PASS'
        }
    
    def check_numeric_ranges(self, rules: Dict[str, tuple]) -> Dict:
        """Проверка диапазонов числовых значений"""
        results = {}
        for col, (min_val, max_val) in rules.items():
            out_of_range = self.df[(self.df[col] < min_val) | (self.df[col] > max_val)]
            results[col] = {
                'out_of_range_count': len(out_of_range),
                'expected_range': (min_val, max_val),
                'actual_min': self.df[col].min(),
                'actual_max': self.df[col].max(),
                'status': 'FAIL' if len(out_of_range) > 0 else 'PASS'
            }
        return results

# Использование
validator = DataQualityValidator(df)
null_results = validator.check_null_ratios({'amount': 5.0, 'customer_id': 0.0})
duplicate_results = validator.check_duplicates(['transaction_id'])
range_results = validator.check_numeric_ranges({'amount': (0, 1000000), 'age': (0, 150)})
```

**Task 2: Document Crawler с полнотекстовым поиском**

```python
# crawler.py - Рекурсивный краулинг файлов
import os
import zipfile
import rarfile
from pathlib import Path

class DocumentCrawler:
    """
    Краулинг различных форматов файлов:
    txt, docx, xlsx, pdf, zip, rar, 7z
    """
    
    SUPPORTED_FORMATS = {'.txt', '.docx', '.xlsx', '.pdf', '.zip', '.rar', '.7z'}
    
    @staticmethod
    def crawl_directory(path: str, recursive=True) -> list:
        """Рекурсивный обход директории"""
        files = []
        for root, dirs, filenames in os.walk(path):
            for filename in filenames:
                if Path(filename).suffix.lower() in DocumentCrawler.SUPPORTED_FORMATS:
                    full_path = os.path.join(root, filename)
                    files.append({
                        'path': full_path,
                        'filename': filename,
                        'size': os.path.getsize(full_path)
                    })
            if not recursive:
                break
        return files
    
    @staticmethod
    def extract_archive(filepath: str) -> list:
        """Распаковка архивов (zip, rar, 7z)"""
        extracted_files = []
        suffix = Path(filepath).suffix.lower()
        
        if suffix == '.zip':
            with zipfile.ZipFile(filepath) as zf:
                extracted_files = zf.namelist()
        # rar и 7z аналогично
        
        return extracted_files
```

```sql
-- PostgreSQL GIN-индекс для полнотекстового поиска
CREATE TABLE documents (
    doc_id SERIAL PRIMARY KEY,
    filename VARCHAR(255),
    content TEXT,
    file_type VARCHAR(10),
    uploaded_at TIMESTAMP DEFAULT NOW(),
    search_vector TSVECTOR
);

-- Создание индекса для быстрого поиска
CREATE INDEX idx_search_vector ON documents USING GIN(search_vector);

-- Триггер для автоматического обновления search_vector
CREATE OR REPLACE FUNCTION update_search_vector()
RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector := to_tsvector('russian', NEW.content);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_search_vector
BEFORE INSERT OR UPDATE ON documents
FOR EACH ROW
EXECUTE FUNCTION update_search_vector();

-- Быстрый полнотекстовый поиск
SELECT doc_id, filename, ts_rank(search_vector, query) as rank
FROM documents,
     plainto_tsquery('russian', 'финансовые операции') as query
WHERE search_vector @@ query
ORDER BY rank DESC
LIMIT 20;
```

**Запуск проекта:**

```bash
cd projects/financial-transactions-analysis

# Task 1: Анализ данных
cd task1_analysis
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
jupyter notebook notebooks/main.ipynb

# Task 2: Краулер + БД
cd ../task2_crawler
docker-compose up -d

# Генерация тестовых файлов
docker-compose run --rm app python scripts/generate_files.py

# Краулинг и загрузка в БД
docker-compose run --rm app python scripts/crawler.py
docker-compose run --rm app python scripts/load_to_db.py

# Проверка загруженных данных
docker-compose run --rm app psql -h postgres -U user bookstore_db \
  -c "SELECT COUNT(*) FROM documents;"

# Cleanup
docker-compose down
```

**GitHub:** [financial-transactions-analysis](./projects/financial-transactions-analysis/)

---

## 🚀 ETL Pipeline с Airflow (NEW)

**Описание:** Production-ready ETL DAG для обработки финансовых данных с логированием, обработкой ошибок и мониторингом качества.

### Архитектура Pipeline:

```
Extract (API/DB) → Transform (Validation) → Load (DWH) → Quality Check
```

**Файл: `dags/financial_etl_dag.py`**

```python
"""
Financial ETL DAG
================
ETL процесс для обработки финансовых транзакций
- Extraction: PostgreSQL source DB
- Transformation: Data cleaning & validation
- Load: Target warehouse
- Quality: Data profiling & checks

Dag ID: financial_transactions_etl
Schedule: Daily at 02:00 UTC
Owner: data-platform-team
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.task_group import TaskGroup
from airflow.models import Variable
import pandas as pd
import logging

# ====== Default Arguments ======
default_args = {
    'owner': 'anna.leonteva',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email': ['anna.leonteva.2016@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'execution_timeout': timedelta(hours=1),
}

# ====== DAG Definition ======
dag = DAG(
    'financial_transactions_etl',
    default_args=default_args,
    description='Daily ETL for financial transactions',
    schedule_interval='0 2 * * *',  # 02:00 UTC daily
    catchup=False,
    tags=['data-engineering', 'financial', 'daily'],
)

logger = logging.getLogger(__name__)

# ====== Extract Functions ======
def extract_from_source_db(**context):
    """
    Извлечение данных из исходной БД
    Сохранение в staging таблицу
    """
    import psycopg2
    from psycopg2.extras import RealDictCursor
    
    logger.info("Starting data extraction from source database...")
    
    source_conn = psycopg2.connect(
        host=Variable.get('source_db_host'),
        database=Variable.get('source_db_name'),
        user=Variable.get('source_db_user'),
        password=Variable.get('source_db_password')
    )
    
    execution_date = context['execution_date']
    query = f"""
    SELECT 
        transaction_id,
        customer_id,
        amount,
        transaction_date,
        merchant_category,
        status
    FROM transactions
    WHERE DATE(transaction_date) = '{execution_date.date()}'
    """
    
    df = pd.read_sql(query, source_conn)
    logger.info(f"Extracted {len(df)} rows from source DB")
    
    # Сохранение в Airflow XCom для передачи между tasks
    context['task_instance'].xcom_push(key='extracted_rows', value=len(df))
    
    # Сохранение в CSV для следующего stage
    df.to_csv('/tmp/extracted_transactions.csv', index=False)
    logger.info("Data saved to staging CSV")
    
    source_conn.close()
    return len(df)


def validate_extracted_data(**context):
    """
    Валидация извлеченных данных
    Проверка null values, duplicates, data types
    """
    logger.info("Validating extracted data...")
    
    df = pd.read_csv('/tmp/extracted_transactions.csv')
    validation_errors = []
    
    # Проверка 1: NULL значения
    null_thresholds = {
        'transaction_id': 0.0,
        'customer_id': 0.0,
        'amount': 5.0,
        'transaction_date': 0.0,
    }
    
    for col, threshold in null_thresholds.items():
        null_pct = df[col].isna().sum() / len(df) * 100
        if null_pct > threshold:
            validation_errors.append(
                f"Column {col}: {null_pct:.2f}% NULLs (threshold: {threshold}%)"
            )
    
    # Проверка 2: Дубликаты
    duplicates = df[['transaction_id']].duplicated().sum()
    if duplicates > 0:
        validation_errors.append(f"Found {duplicates} duplicate transaction_ids")
    
    # Проверка 3: Диапазоны числовых значений
    if (df['amount'] < 0).any():
        validation_errors.append("Amount values < 0 found")
    
    if validation_errors:
        logger.error("Validation errors:\n" + "\n".join(validation_errors))
        raise Exception("Data validation failed")
    
    logger.info(f"✅ Data validation passed. Rows: {len(df)}")
    context['task_instance'].xcom_push(key='validation_status', value='PASSED')
    
    return True


def transform_transactions(**context):
    """
    Трансформация данных:
    - Очистка
    - Обогащение (категории, сегменты)
    - Расчет агрегатов
    """
    logger.info("Transforming transaction data...")
    
    df = pd.read_csv('/tmp/extracted_transactions.csv')
    
    # Трансформация 1: Очистка и типизация
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    df['amount'] = df['amount'].astype(float)
    df['customer_id'] = df['customer_id'].astype(int)
    
    # Трансформация 2: Обогащение данных
    df['amount_category'] = pd.cut(
        df['amount'],
        bins=[0, 1000, 10000, float('inf')],
        labels=['Small', 'Medium', 'Large']
    )
    
    df['hour_of_day'] = df['transaction_date'].dt.hour
    df['day_of_week'] = df['transaction_date'].dt.dayofweek
    
    # Трансформация 3: Flagging для дальнейшего анализа
    df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
    df['is_high_value'] = (df['amount'] > df['amount'].quantile(0.75)).astype(int)
    
    logger.info(f"Transformed {len(df)} rows")
    logger.info(f"Data shape: {df.shape}")
    
    # Сохранение трансформированных данных
    df.to_csv('/tmp/transformed_transactions.csv', index=False)
    context['task_instance'].xcom_push(key='transformed_rows', value=len(df))
    
    return True


def calculate_aggregates(**context):
    """
    Расчет агрегатов и витрин данных
    (как окончательный слой в DWH)
    """
    logger.info("Calculating aggregate tables...")
    
    df = pd.read_csv('/tmp/transformed_transactions.csv')
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    
    # Витрина 1: Daily summary
    daily_summary = df.groupby(df['transaction_date'].dt.date).agg({
        'transaction_id': 'count',
        'amount': ['sum', 'mean', 'min', 'max'],
        'customer_id': 'nunique'
    }).reset_index()
    
    daily_summary.columns = [
        'transaction_date', 'transaction_count', 'total_amount',
        'avg_amount', 'min_amount', 'max_amount', 'unique_customers'
    ]
    
    # Витрина 2: Customer aggregates (RFM)
    customer_agg = df.groupby('customer_id').agg({
        'transaction_id': 'count',
        'amount': ['sum', 'mean'],
        'transaction_date': 'max'
    }).reset_index()
    
    customer_agg.columns = [
        'customer_id', 'purchase_count', 'lifetime_value',
        'avg_transaction_amount', 'last_transaction_date'
    ]
    
    logger.info(f"Daily summary rows: {len(daily_summary)}")
    logger.info(f"Customer aggregate rows: {len(customer_agg)}")
    
    daily_summary.to_csv('/tmp/daily_summary.csv', index=False)
    customer_agg.to_csv('/tmp/customer_aggregates.csv', index=False)
    
    return True


# ====== Load Functions ======
def load_to_warehouse(**context):
    """
    Загрузка трансформированных данных в DWH
    (PostgreSQL, Vertica, ClickHouse)
    """
    import psycopg2
    
    logger.info("Loading data to warehouse...")
    
    df = pd.read_csv('/tmp/transformed_transactions.csv')
    
    warehouse_conn = psycopg2.connect(
        host=Variable.get('warehouse_db_host'),
        database=Variable.get('warehouse_db_name'),
        user=Variable.get('warehouse_db_user'),
        password=Variable.get('warehouse_db_password')
    )
    
    cursor = warehouse_conn.cursor()
    
    # Загрузка в DWH таблицу
    for idx, row in df.iterrows():
        insert_query = """
        INSERT INTO dwh.fact_transactions 
        (transaction_id, customer_id, amount, transaction_date, merchant_category, 
         status, amount_category, hour_of_day, is_weekend, is_high_value)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (transaction_id) DO UPDATE SET updated_at = NOW()
        """
        
        cursor.execute(insert_query, (
            row['transaction_id'], row['customer_id'], row['amount'],
            row['transaction_date'], row['merchant_category'], row['status'],
            row['amount_category'], row['hour_of_day'], row['is_weekend'],
            row['is_high_value']
        ))
    
    warehouse_conn.commit()
    logger.info(f"✅ Loaded {len(df)} rows to warehouse")
    
    cursor.close()
    warehouse_conn.close()
    
    return len(df)


# ====== Quality Checks ======
def data_quality_check(**context):
    """
    Post-load проверки качества данных
    (как в требованиях Ozon)
    """
    logger.info("Running data quality checks...")
    
    import psycopg2
    
    warehouse_conn = psycopg2.connect(
        host=Variable.get('warehouse_db_host'),
        database=Variable.get('warehouse_db_name'),
        user=Variable.get('warehouse_db_user'),
        password=Variable.get('warehouse_db_password')
    )
    
    cursor = warehouse_conn.cursor()
    
    # Проверка 1: Количество загруженных строк
    cursor.execute("""
    SELECT COUNT(*) FROM dwh.fact_transactions 
    WHERE DATE(transaction_date) = CURRENT_DATE
    """)
    
    loaded_count = cursor.fetchone()[0]
    expected_count = context['task_instance'].xcom_pull(
        task_ids='validate_extracted_data', key='validation_status'
    )
    
    logger.info(f"Loaded rows: {loaded_count}")
    
    # Проверка 2: NULL values в критических полях
    cursor.execute("""
    SELECT 
        SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) as null_customer_id,
        SUM(CASE WHEN amount IS NULL THEN 1 ELSE 0 END) as null_amount,
        SUM(CASE WHEN transaction_date IS NULL THEN 1 ELSE 0 END) as null_date
    FROM dwh.fact_transactions
    WHERE DATE(transaction_date) = CURRENT_DATE
    """)
    
    null_counts = cursor.fetchone()
    if any(null_counts):
        logger.warning(f"Found NULL values: customer_id={null_counts[0]}, "
                      f"amount={null_counts[1]}, date={null_counts[2]}")
    
    # Проверка 3: Диапазоны значений
    cursor.execute("""
    SELECT 
        MIN(amount) as min_amount,
        MAX(amount) as max_amount,
        AVG(amount) as avg_amount
    FROM dwh.fact_transactions
    WHERE DATE(transaction_date) = CURRENT_DATE
    """)
    
    stats = cursor.fetchone()
    logger.info(f"Amount stats - Min: {stats[0]}, Max: {stats[1]}, Avg: {stats[2]:.2f}")
    
    if stats[0] < 0:
        raise Exception("Negative amounts detected!")
    
    logger.info("✅ All data quality checks passed")
    
    cursor.close()
    warehouse_conn.close()
    
    return True


# ====== DAG Tasks ======

with dag:
    
    # Информационная задача
    log_task_start = BashOperator(
        task_id='log_task_start',
        bash_command='echo "Starting Financial ETL Pipeline at $(date)"'
    )
    
    # ========== EXTRACT STAGE ==========
    with TaskGroup(group_id='extract_stage') as extract_group:
        
        extract_task = PythonOperator(
            task_id='extract_from_source_db',
            python_callable=extract_from_source_db,
            provide_context=True,
        )
        
        validate_task = PythonOperator(
            task_id='validate_extracted_data',
            python_callable=validate_extracted_data,
            provide_context=True,
        )
        
        extract_task >> validate_task
    
    # ========== TRANSFORM STAGE ==========
    with TaskGroup(group_id='transform_stage') as transform_group:
        
        transform_task = PythonOperator(
            task_id='transform_transactions',
            python_callable=transform_transactions,
            provide_context=True,
        )
        
        aggregate_task = PythonOperator(
            task_id='calculate_aggregates',
            python_callable=calculate_aggregates,
            provide_context=True,
        )
        
        transform_task >> aggregate_task
    
    # ========== LOAD STAGE ==========
    with TaskGroup(group_id='load_stage') as load_group:
        
        load_task = PythonOperator(
            task_id='load_to_warehouse',
            python_callable=load_to_warehouse,
            provide_context=True,
        )
        
        quality_check_task = PythonOperator(
            task_id='data_quality_check',
            python_callable=data_quality_check,
            provide_context=True,
        )
        
        load_task >> quality_check_task
    
    # ========== Task Dependencies ==========
    log_task_start >> extract_group >> transform_group >> load_group
```

**Запуск Airflow локально:**

```bash
# 1. Установка Airflow
pip install apache-airflow

# 2. Инициализация БД Airflow
airflow db init

# 3. Создание пользователя
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com

# 4. Копирование DAG в папку
mkdir -p ~/airflow/dags
cp dags/financial_etl_dag.py ~/airflow/dags/

# 5. Запуск scheduler и web server
airflow scheduler &
airflow webserver --port 8080

# 6. Доступ к UI
# http://localhost:8080 (login: admin)

# 7. Запуск DAG вручную (тестирование)
airflow dags test financial_transactions_etl 2024-01-15

# 8. Просмотр логов
airflow logs -f financial_transactions_etl extract_stage.extract_from_source_db
```

**GitHub:** [airflow-dags](./projects/airflow-dags/)

---

## 💾 SQL Examples — Window Functions & Advanced

### 1. RFM-сегментация с NTILE()

```sql
WITH rfm_calculation AS (
    SELECT 
        c.customer_id,
        c.customer_name,
        MAX(o.order_date) as last_order_date,
        COUNT(DISTINCT o.order_id) as order_count,
        SUM(o.order_amount) as total_spent,
        
        -- Recency: как давно последний заказ
        DATEDIFF(DAY, MAX(o.order_date), CURRENT_DATE) as days_since_order,
        
        -- Quintiles для каждого метрика
        NTILE(5) OVER (ORDER BY MAX(o.order_date) DESC) as r_quintile,
        NTILE(5) OVER (ORDER BY COUNT(DISTINCT o.order_id) DESC) as f_quintile,
        NTILE(5) OVER (ORDER BY SUM(o.order_amount) DESC) as m_quintile
        
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_name
)
SELECT 
    customer_id,
    customer_name,
    last_order_date,
    order_count,
    total_spent,
    CASE 
        WHEN r_quintile <= 2 AND f_quintile >= 4 AND m_quintile >= 4 THEN 'Champions'
        WHEN r_quintile <= 2 AND f_quintile >= 3 THEN 'Loyal Customers'
        WHEN r_quintile <= 3 THEN 'Potential Loyalists'
        WHEN m_quintile >= 4 THEN 'Can\'t Lose Them'
        ELSE 'At Risk'
    END as customer_segment
FROM rfm_calculation
ORDER BY customer_segment, total_spent DESC;
```

### 2. Running Total с SUM OVER

```sql
-- Кумулятивная сумма доходов по дням
SELECT 
    transaction_date,
    amount,
    SUM(amount) OVER (
        ORDER BY transaction_date 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as cumulative_amount,
    
    -- Running total по customer
    SUM(amount) OVER (
        PARTITION BY customer_id 
        ORDER BY transaction_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as customer_lifetime_value,
    
    -- Moving average (7-day)
    AVG(amount) OVER (
        ORDER BY transaction_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as moving_avg_7day
    
FROM transactions
ORDER BY transaction_date DESC;
```

### 3. Ranking с RANK() / DENSE_RANK() / ROW_NUMBER()

```sql
-- Рейтинг товаров по выручке
SELECT 
    product_id,
    product_name,
    revenue,
    
    -- Обычный рейтинг (есть пробелы)
    RANK() OVER (ORDER BY revenue DESC) as rank_with_gaps,
    
    -- Плотный рейтинг (без пробелов)
    DENSE_RANK() OVER (ORDER BY revenue DESC) as rank_no_gaps,
    
    -- Строгая нумерация
    ROW_NUMBER() OVER (ORDER BY revenue DESC) as row_num,
    
    -- Top product по категории
    ROW_NUMBER() OVER (
        PARTITION BY category 
        ORDER BY revenue DESC
    ) as rank_in_category
    
FROM products
WHERE revenue > 0
ORDER BY revenue DESC;
```

### 4. Complex JOINs (LEFT + INNER)

```sql
-- Запрос: все клиенты + их заказы + товары в заказах
SELECT 
    c.customer_id,
    c.customer_name,
    c.country,
    o.order_id,
    o.order_date,
    oi.product_id,
    p.product_name,
    oi.quantity,
    oi.unit_price,
    (oi.quantity * oi.unit_price) as line_total,
    
    -- Aggregate статистика
    COUNT(DISTINCT o.order_id) OVER (PARTITION BY c.customer_id) as customer_order_count,
    SUM(oi.quantity * oi.unit_price) OVER (PARTITION BY c.customer_id) as customer_total_spent
    
FROM customers c
LEFT JOIN orders o 
    ON c.customer_id = o.customer_id
    AND o.order_date >= DATEADD(YEAR, -1, CURRENT_DATE)
LEFT JOIN order_items oi 
    ON o.order_id = oi.order_id
INNER JOIN products p 
    ON oi.product_id = p.product_id
    AND p.is_active = 1
    
WHERE c.country IN ('Russia', 'Belarus', 'Kazakhstan')
ORDER BY c.customer_id, o.order_date DESC;
```

### 5. CTE (Common Table Expressions)

```sql
-- Пример: найти "спящих" клиентов, готовых к win-back кампании
WITH customer_activity AS (
    -- Последняя активность каждого клиента
    SELECT 
        customer_id,
        MAX(order_date) as last_order_date,
        COUNT(*) as order_count,
        SUM(order_amount) as lifetime_value
    FROM orders
    GROUP BY customer_id
),
dormant_customers AS (
    -- Клиенты без заказов > 6 месяцев
    SELECT 
        customer_id,
        last_order_date,
        lifetime_value,
        DATEDIFF(DAY, last_order_date, CURRENT_DATE) as days_inactive
    FROM customer_activity
    WHERE last_order_date < DATEADD(MONTH, -6, CURRENT_DATE)
      AND lifetime_value > 1000  -- Когда-то покупали товарный запас
),
win_back_cohorts AS (
    -- Группировка по периодам неактивности
    SELECT 
        customer_id,
        CASE 
            WHEN days_inactive BETWEEN 180 AND 365 THEN '6-12 months'
            WHEN days_inactive BETWEEN 365 AND 730 THEN '1-2 years'
            ELSE '2+ years'
        END as dormancy_period,
        lifetime_value,
        ROW_NUMBER() OVER (
            PARTITION BY CASE 
                WHEN days_inactive BETWEEN 180 AND 365 THEN '6-12 months'
                WHEN days_inactive BETWEEN 365 AND 730 THEN '1-2 years'
                ELSE '2+ years'
            END
            ORDER BY lifetime_value DESC
        ) as rank_in_cohort
    FROM dormant_customers
)
SELECT 
    customer_id,
    dormancy_period,
    lifetime_value,
    rank_in_cohort
FROM win_back_cohorts
WHERE rank_in_cohort <= 100  -- Top 100 в каждом cohort
ORDER BY dormancy_period, rank_in_cohort;
```

---

## 🔄 DevOps & Infrastructure

### 2. Docker & Docker Compose для Data Engineering

**`docker-compose.yml` — локальное окружение DWH:**

```yaml
version: '3.8'

services:
  # PostgreSQL: Source DB + Staging
  source-db:
    image: postgres:15
    container_name: source_db
    environment:
      POSTGRES_DB: source_db
      POSTGRES_USER: data_eng
      POSTGRES_PASSWORD: secure_password_123
    ports:
      - "5432:5432"
    volumes:
      - source_db_volume:/var/lib/postgresql/data
      - ./init-scripts/source-schema.sql:/docker-entrypoint-initdb.d/01-schema.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U data_eng"]
      interval: 10s
      timeout: 5s
      retries: 5

  # PostgreSQL: Target DWH
  warehouse-db:
    image: postgres:15
    container_name: warehouse_db
    environment:
      POSTGRES_DB: warehouse_db
      POSTGRES_USER: data_eng
      POSTGRES_PASSWORD: secure_password_123
    ports:
      - "5433:5432"
    volumes:
      - warehouse_db_volume:/var/lib/postgresql/data
      - ./init-scripts/warehouse-schema.sql:/docker-entrypoint-initdb.d/01-schema.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U data_eng"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis: Кэш для Airflow
  redis:
    image: redis:7-alpine
    container_name: airflow_redis
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Airflow: Orchestration
  airflow:
    image: apache/airflow:2.7.0
    container_name: airflow_scheduler
    depends_on:
      - source-db
      - warehouse-db
      - redis
    environment:
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql://data_eng:secure_password_123@source-db:5432/airflow
      AIRFLOW__CELERY__BROKER_URL: redis://redis:6379/0
      AIRFLOW__CELERY__RESULT_BACKEND: postgresql://data_eng:secure_password_123@source-db:5432/airflow
      AIRFLOW__CORE__EXECUTOR: CeleryExecutor
    ports:
      - "8080:8080"
    volumes:
      - ./dags:/opt/airflow/dags
      - ./logs:/opt/airflow/logs
      - ./plugins:/opt/airflow/plugins
    command: >
      sh -c "airflow db init && 
             airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com || true &&
             airflow scheduler"

volumes:
  source_db_volume:
  warehouse_db_volume:

networks:
  default:
    name: dwh-network
```

**Запуск:**

```bash
# Развертывание окружения
docker-compose up -d

# Проверка статуса
docker-compose ps

# Доступ к PostgreSQL
docker-compose exec source-db psql -U data_eng -d source_db

# Просмотр логов
docker-compose logs -f airflow

# Остановка
docker-compose down -v
```

### 3. CI/CD Pipeline для Data Projects

**`.github/workflows/data-pipeline-ci.yml`:**

```yaml
name: Data Pipeline CI/CD

on:
  push:
    branches: [ main, develop ]
    paths:
      - 'dags/**'
      - 'src/**'
      - 'tests/**'
      - 'requirements.txt'
  pull_request:
    branches: [ main ]

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: [3.9, '3.10', '3.11']
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
        cache: 'pip'
    
    - name: Install dependencies
      run: |
        pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pylint black flake8
    
    - name: Code Linting
      run: |
        flake8 src/ dags/ --count --show-source --statistics
        pylint src/ dags/ --fail-under=8.0
    
    - name: Code Formatting Check
      run: black --check src/ dags/
    
    - name: SQL Validation
      run: |
        pip install sqlparse
        python scripts/validate_sql.py sql/
    
    - name: Unit Tests
      run: |
        pytest tests/ -v --cov=src --cov-report=xml
    
    - name: Upload Coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  security-scan:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Run Bandit (SAST)
      run: |
        pip install bandit
        bandit -r src/ dags/ -f json -o bandit-report.json
    
    - name: Check for Secrets (Gitleaks)
      uses: gitleaks/gitleaks-action@v2
    
    - name: Dependency Check
      run: |
        pip install pip-audit
        pip-audit --desc

  docker-build:
    runs-on: ubuntu-latest
    needs: lint-and-test
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Build Docker Image
      run: |
        docker build -t ghcr.io/${{ github.repository }}/data-pipeline:latest .
    
    - name: Scan Docker Image
      run: |
        docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
          aquasec/trivy image ghcr.io/${{ github.repository }}/data-pipeline:latest
    
    - name: Push to GHCR
      run: |
        echo ${{ secrets.GITHUB_TOKEN }} | docker login ghcr.io -u ${{ github.actor }} --password-stdin
        docker push ghcr.io/${{ github.repository }}/data-pipeline:latest
```

---

## 📚 DevOps & Best Practices

Полный курс "Программная инженерия: Введение в DevOps" (8 практик, 2026 год)

### Практики, применимые в Data Engineering:

| Практика | Что изучалось | Применение в DE |
|----------|--------------|-----------------|
| **Practice 202: CI/CD** | GitHub Actions, branch protection, pre-commit | Автоматизация запуска ETL DAG'ов |
| **Practice 203: Docker** | Multi-stage builds, docker-compose, registry | Контейнеризация Airflow, DWH |
| **Practice 204: Terraform** | IaC, state management, modules | Развертывание облачных ресурсов |
| **Practice 205: Optimization** | Caching, matrix testing, security | Оптимизация времени ETL |
| **Practice 206: Monitoring** | Alerting, logging, DORA metrics | Мониторинг пайплайнов |
| **Practice 207: DevSecOps** | Trivy, Bandit, secret scanning | Защита данных, SBOM |
| **Practice 208: Cloud** | AWS/GCP/Azure/Yandex | DWH на облаке |

**Репозиторий:** [devops-practices](./devops-practices/)

---

## 🧠 Ключевые компетенции

### Database Theory (Базы данных)
- ✅ Нормализация (1NF, 2NF, 3NF, BCNF)
- ✅ Индексирование (B-tree, Hash, GIN, BRIN)
- ✅ Query optimization (EXPLAIN ANALYZE)
- ✅ Transaction management (ACID, isolation levels)

### SQL
- ✅ SELECT с WHERE, ORDER BY, GROUP BY
- ✅ Window Functions (RANK, ROW_NUMBER, SUM OVER, NTILE)
- ✅ JOINs (INNER, LEFT, RIGHT, FULL OUTER, CROSS)
- ✅ CTEs (WITH clauses)
- ✅ Aggregations и subqueries
- ✅ PostgreSQL specific (TSVECTOR, JSON, arrays)

### Python for Data
- ✅ pandas (DataFrames, groupby, merge, pivot)
- ✅ scikit-learn (preprocessing, modeling)
- ✅ NumPy (vectorization)
- ✅ Logging и error handling
- ✅ Data validation и profiling

### ETL/ELT & Data Pipelines
- ✅ Extraction (APIs, databases, files)
- ✅ Transformation (cleaning, aggregation, enrichment)
- ✅ Loading (incremental vs full load, upserts)
- ✅ Data quality checks
- ✅ Monitoring и alerting

### DevOps & Infrastructure
- ✅ Docker & Docker Compose
- ✅ Git workflows (trunk-based development)
- ✅ CI/CD (GitHub Actions)
- ✅ Bash scripting
- ✅ Cloud basics (Yandex Cloud preferred)

---

## 🚀 Quick Start для проектов

### Bookstore Analytics:
```bash
cd projects/bookstore-analytics
docker-compose up -d
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
jupyter notebook stage3_analysis.ipynb
```

### Financial Analysis:
```bash
cd projects/financial-transactions-analysis/task2_crawler
docker-compose up -d
docker-compose run --rm app python scripts/crawler.py
docker-compose run --rm app python scripts/load_to_db.py
```

### Airflow ETL:
```bash
pip install apache-airflow
airflow db init
cp dags/*.py ~/airflow/dags/
airflow webserver --port 8080 &
airflow scheduler
# http://localhost:8080
```

---

## 📊 DORA Metrics

- **Lead Time**: < 1 дня (от commit до production)
- **Deployment Frequency**: 1x в день
- **Change Failure Rate**: < 15%
- **MTTR**: < 1 часа

---

## 🔗 Ссылки

- 🐙 GitHub: [@Ubnubn2](https://github.com/Ubnubn2)
- 💼 LinkedIn: [Анна Леонтьева](https://linkedin.com/in/anna-leonteva)
- 📧 Email: anna.leonteva.2016@gmail.com

---

**Last Updated:** January 2024 | Powered by Python, PostgreSQL, Airflow