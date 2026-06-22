-- 1. Топ-10 самых продаваемых книг
SELECT 
    b.title,
    a.name as author,
    SUM(od.quantity * od.price) as revenue,
    SUM(od.quantity) as total_sold
FROM books b
JOIN authors a ON b.author_id = a.author_id
JOIN order_details od ON b.book_id = od.book_id
GROUP BY b.title, a.name
ORDER BY revenue DESC
LIMIT 10;

-- 2. Динамика продаж по месяцам
SELECT 
    DATE_TRUNC('month', order_date) as month,
    COUNT(*) as orders_count,
    SUM(total_amount) as total_revenue,
    AVG(total_amount) as avg_order_value,
    SUM(SUM(total_amount)) OVER (ORDER BY DATE_TRUNC('month', order_date)) as cumulative_revenue
FROM orders
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;

-- 3. Топ-10 клиентов по сумме покупок
SELECT 
    c.name,
    c.email,
    c.city,
    COUNT(o.order_id) as orders_count,
    SUM(o.total_amount) as total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name, c.email, c.city
ORDER BY total_spent DESC
LIMIT 10;

-- 4. Самые популярные авторы
SELECT 
    a.name,
    COUNT(DISTINCT b.book_id) as books_count,
    SUM(od.quantity) as copies_sold,
    SUM(od.quantity * od.price) as revenue
FROM authors a
JOIN books b ON a.author_id = b.author_id
JOIN order_details od ON b.book_id = od.book_id
GROUP BY a.author_id, a.name
ORDER BY revenue DESC
LIMIT 10;

-- 5. Проверочный запрос (количество книг)
SELECT COUNT(*) as total_books FROM books;
        