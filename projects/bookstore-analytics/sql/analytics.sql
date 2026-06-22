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
         
-- ====================================================== 
-- RFM-������ 
WITH customer_metrics AS (
    SELECT
        c.customer_id,
        c.name,
        EXTRACT(DAY FROM (CURRENT_DATE - MAX(o.order_date))) AS recency_days,
        COUNT(o.order_id) AS frequency,
        SUM(o.total_amount) AS monetary
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.name
),
percentiles AS (
    SELECT
        customer_id,
        name,
        recency_days,
        frequency,
        monetary,
        NTILE(5) OVER (ORDER BY recency_days DESC) AS r_score,
        NTILE(5) OVER (ORDER BY frequency) AS f_score,
        NTILE(5) OVER (ORDER BY monetary) AS m_score
    FROM customer_metrics
    WHERE recency_days IS NOT NULL
)
SELECT
    customer_id,
    name,
    recency_days,
    frequency,
    monetary,
    r_score,
    f_score,
    m_score,
    CONCAT(r_score, f_score, m_score) AS rfm_segment,
    CASE
        WHEN r_score = 5 AND f_score = 5 AND m_score = 5 THEN 'Чемпионы'
        WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Лояльные'
        WHEN r_score >= 3 AND f_score >= 3 AND m_score >= 3 THEN 'Потенциальные'
        WHEN r_score <= 2 AND f_score <= 2 AND m_score <= 2 THEN 'Спящие'
        ELSE 'Смешанный'
    END AS segment_name
FROM percentiles
ORDER BY r_score DESC, f_score DESC, m_score DESC; 
-- ���।������ �� ��� ������ 
SELECT
    EXTRACT(DOW FROM order_date) AS day_of_week_number,
    TO_CHAR(order_date, 'Day') AS day_name,
    COUNT(*) AS orders_count,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_order_value
FROM orders
GROUP BY EXTRACT(DOW FROM order_date), TO_CHAR(order_date, 'Day')
ORDER BY day_of_week_number;
 
-- ������� 
CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_order_details_order_id ON order_details(order_id);
CREATE INDEX IF NOT EXISTS idx_order_details_book_id ON order_details(book_id);
CREATE INDEX IF NOT EXISTS idx_books_author_id ON books(author_id);
CREATE INDEX IF NOT EXISTS idx_orders_order_date ON orders(order_date);
 
-- EXPLAIN ANALYZE 
EXPLAIN ANALYZE
SELECT b.title, SUM(od.quantity * od.price) as revenue
FROM books b
JOIN order_details od ON b.book_id = od.book_id
GROUP BY b.title
ORDER BY revenue DESC
LIMIT 10;