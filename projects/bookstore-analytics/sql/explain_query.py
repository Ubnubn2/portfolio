from sqlalchemy import create_engine, text

engine = create_engine('postgresql://postgres:mysecretpassword@localhost:5432/postgres')

query = """
EXPLAIN ANALYZE
SELECT b.title, SUM(od.quantity * od.price) as revenue
FROM books b
JOIN order_details od ON b.book_id = od.book_id
GROUP BY b.title
ORDER BY revenue DESC
LIMIT 10;
"""

with engine.connect() as conn:
    result = conn.execute(text(query))
    for row in result:
        print(row[0])