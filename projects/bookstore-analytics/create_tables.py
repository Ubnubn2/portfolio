import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine('postgresql://postgres:mysecretpassword@localhost:5432/postgres')

with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS authors (
            author_id SERIAL PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            birth_year INT
        );
    """))
    
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS books (
            book_id SERIAL PRIMARY KEY,
            title VARCHAR(300) NOT NULL,
            price DECIMAL(10,2),
            publication_year INT,
            author_id INT REFERENCES authors(author_id)
        );
    """))
    
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id SERIAL PRIMARY KEY,
            name VARCHAR(200),
            email VARCHAR(200) UNIQUE,
            city VARCHAR(100),
            registration_date DATE
        );
    """))
    
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id SERIAL PRIMARY KEY,
            customer_id INT REFERENCES customers(customer_id),
            order_date DATE,
            total_amount DECIMAL(10,2)
        );
    """))
    
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS order_details (
            order_detail_id SERIAL PRIMARY KEY,
            order_id INT REFERENCES orders(order_id),
            book_id INT REFERENCES books(book_id),
            quantity INT,
            price DECIMAL(10,2)
        );
    """))
    
    conn.commit()
    print("Таблицы созданы.")