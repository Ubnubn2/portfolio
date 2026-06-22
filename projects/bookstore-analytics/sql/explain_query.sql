EXPLAIN ANALYZE
SELECT b.title, SUM(od.quantity * od.price) as revenue
FROM books b
JOIN order_details od ON b.book_id = od.book_id
GROUP BY b.title
ORDER BY revenue DESC
LIMIT 10;