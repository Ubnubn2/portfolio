import os
import psycopg2
import pandas as pd

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', 5432),
    'database': os.getenv('DB_NAME', 'search_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'mysecretpassword')
}

def main():
    print("Чтение data/crawled_data.csv...")
    df = pd.read_csv('data/crawled_data.csv')
    print(f"Загружено {len(df)} записей.")

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute('''
        DROP TABLE IF EXISTS files CASCADE;
        CREATE TABLE files (
            id SERIAL PRIMARY KEY,
            file_path TEXT,
            file_name TEXT,
            file_type TEXT,
            content TEXT
        );
    ''')

    print("Загрузка данных в таблицу files...")
    for _, row in df.iterrows():
        cur.execute('''
            INSERT INTO files (file_path, file_name, file_type, content)
            VALUES (%s, %s, %s, %s)
        ''', (row['file_path'], row['file_name'], row['file_type'], row['content']))
    conn.commit()
    print("Данные загружены.")

    print("Создание полнотекстового индекса...")
    cur.execute('''
        ALTER TABLE files ADD COLUMN IF NOT EXISTS content_tsv tsvector;
        UPDATE files SET content_tsv = 
            setweight(to_tsvector('russian', coalesce(content,'')), 'A') ||
            setweight(to_tsvector('english', coalesce(content,'')), 'B');
        CREATE INDEX IF NOT EXISTS files_content_gin_idx ON files USING GIN (content_tsv);
    ''')
    conn.commit()
    print("Индекс создан.")

    def search(query):
        cur.execute('''
            SELECT 
                file_path,
                file_name,
                ts_headline('russian', content, plainto_tsquery('russian', %s), 
                           'MaxWords=20, MinWords=10, HighlightAll=FALSE') as snippet
            FROM files
            WHERE content_tsv @@ plainto_tsquery('russian', %s)
            ORDER BY ts_rank(content_tsv, plainto_tsquery('russian', %s)) DESC
            LIMIT 10;
        ''', (query, query, query))
        return cur.fetchall()

    # Тестовый поиск
    test_word = 'John'
    print(f"\n🔍 Пример поиска по слову '{test_word}':")
    results = search(test_word)
    if results:
        for res in results:
            print(f"📄 {res[0]} — {res[1]}")
            print(f"   {res[2][:200]}...\n")
    else:
        print("Ничего не найдено. Попробуйте другое слово вручную.")

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()