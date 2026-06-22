import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine('postgresql://postgres:mysecretpassword@localhost:5432/postgres')

with open('day1_queries.sql', 'r', encoding='utf-8') as f:
    queries = f.read().split(';')  # разделяем по точкам с запятой

for i, query in enumerate(queries):
    if query.strip():
        print(f"Выполняю запрос {i+1}...")
        df = pd.read_sql(query, engine)
        print(df.head())
        print("\n")