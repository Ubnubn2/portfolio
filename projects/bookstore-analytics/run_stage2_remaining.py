import pandas as pd
from sqlalchemy import create_engine, text
import os

engine = create_engine('postgresql://postgres:mysecretpassword@localhost:5432/postgres')

sql_files = [
    'sql/rfm_analysis.sql',
    'sql/weekday_distribution.sql',
    'sql/indices.sql',
    'sql/explain_query.sql'
]

for file in sql_files:
    if not os.path.exists(file):
        print(f"Файл {file} не найден, пропускаем...")
        continue
    print(f"\n--- Выполняю {file} ---")
    with open(file, 'r', encoding='utf-8') as f:
        queries = f.read().split(';')
        for i, query in enumerate(queries):
            query = query.strip()
            if query:
                try:
                    if query.upper().startswith('CREATE INDEX'):
                        with engine.connect() as conn:
                            conn.execute(text(query))
                            conn.commit()
                        print(f"Индекс {i+1} создан.")
                    elif query.upper().startswith('EXPLAIN'):
                        with engine.connect() as conn:
                            result = conn.execute(text(query))
                            print("План выполнения:")
                            for row in result:
                                print(row[0])
                    else:
                        df = pd.read_sql(query, engine)
                        print(df.head(10))
                        # сохраняем результаты для отчёта
                        df.to_csv(f"sql/result_{os.path.basename(file)}_{i}.csv", index=False)
                except Exception as e:
                    print(f"Ошибка в запросе {i+1}: {e}")

print("\nВсе оставшиеся задачи выполнены.")