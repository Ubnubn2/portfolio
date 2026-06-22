import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:mysecretpassword@localhost:5432/postgres')
df = pd.read_sql('SELECT COUNT(*) FROM books;', engine)
print(f"Количество книг: {df.iloc[0, 0]}")