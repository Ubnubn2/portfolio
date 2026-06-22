import pandas as pd
from sqlalchemy import create_engine, text
from faker import Faker
import random

fake = Faker('ru_RU')
engine = create_engine('postgresql://postgres:mysecretpassword@localhost:5432/postgres')

# Проверяем, есть ли уже данные в таблицах
def is_table_empty(table_name):
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
        count = result.scalar()
        return count == 0

# Очищаем таблицы в правильном порядке (сначала зависимые)
def clear_tables():
    with engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE order_details CASCADE;"))
        conn.execute(text("TRUNCATE TABLE orders CASCADE;"))
        conn.execute(text("TRUNCATE TABLE books CASCADE;"))
        conn.execute(text("TRUNCATE TABLE authors CASCADE;"))
        conn.execute(text("TRUNCATE TABLE customers CASCADE;"))
        conn.commit()
    print("Таблицы очищены.")

# Спрашиваем пользователя, хочет ли он очистить таблицы
response = input("Очистить таблицы перед генерацией? (y/n): ").lower()
if response == 'y':
    clear_tables()
    print("Начинаем генерацию данных...")

# Генерация авторов
if is_table_empty('authors'):
    authors = [{'name': fake.name(), 'birth_year': random.randint(1950, 2000)} for _ in range(100)]
    df_authors = pd.DataFrame(authors)
    df_authors.to_sql('authors', engine, if_exists='append', index=False)
    print("Авторы сгенерированы.")
else:
    print("Авторы уже есть.")

# Получаем ID авторов
author_ids = pd.read_sql("SELECT author_id FROM authors", engine)['author_id'].tolist()

# Генерация книг
if is_table_empty('books'):
    books = []
    for _ in range(500):
        books.append({
            'title': fake.catch_phrase(),
            'price': round(random.uniform(200, 1500), 2),
            'publication_year': random.randint(1990, 2024),
            'author_id': random.choice(author_ids)
        })
    df_books = pd.DataFrame(books)
    df_books.to_sql('books', engine, if_exists='append', index=False)
    print("Книги сгенерированы.")
else:
    print("Книги уже есть.")

# Генерация клиентов
if is_table_empty('customers'):
    customers = []
    for _ in range(200):
        customers.append({
            'name': fake.name(),
            'email': fake.email(),
            'city': fake.city(),
            'registration_date': fake.date_between(start_date='-3y', end_date='today')
        })
    df_customers = pd.DataFrame(customers)
    df_customers.to_sql('customers', engine, if_exists='append', index=False)
    print("Клиенты сгенерированы.")
else:
    print("Клиенты уже есть.")

customer_ids = pd.read_sql("SELECT customer_id FROM customers", engine)['customer_id'].tolist()
book_data = pd.read_sql("SELECT book_id, price FROM books", engine)

# Генерация заказов и деталей
if is_table_empty('orders'):
    print("Генерация заказов...")
    for i in range(1000):  # создаём 1000 заказов
        if i % 100 == 0:
            print(f"Обработано {i} заказов...")
        
        customer_id = random.choice(customer_ids)
        order_date = fake.date_between(start_date='-2y', end_date='today')
        total = 0.0
        items = []
        num_items = random.randint(1, 5)
        
        for __ in range(num_items):
            book = book_data.sample(1).iloc[0]
            qty = random.randint(1, 3)
            price = float(book['price'])  # явное преобразование в float
            total += qty * price
            items.append({
                'book_id': int(book['book_id']),
                'quantity': qty,
                'price': price
            })
        
        # Вставляем заказ и сразу получаем его ID
        with engine.connect() as conn:
            result = conn.execute(
                text("INSERT INTO orders (customer_id, order_date, total_amount) VALUES (:cust, :date, :total) RETURNING order_id"),
                {"cust": customer_id, "date": order_date, "total": float(total)}  # явное преобразование в float
            )
            order_id = result.fetchone()[0]
            conn.commit()
        
        # Добавляем детали с полученным order_id
        for item in items:
            with engine.connect() as conn:
                conn.execute(
                    text("INSERT INTO order_details (order_id, book_id, quantity, price) VALUES (:order_id, :book_id, :qty, :price)"),
                    {
                        "order_id": order_id,
                        "book_id": item['book_id'],
                        "qty": item['quantity'],
                        "price": float(item['price'])
                    }
                )
                conn.commit()
    
    print("Заказы и детали успешно сгенерированы.")
else:
    print("Заказы уже есть.")

print("Генерация данных завершена.")