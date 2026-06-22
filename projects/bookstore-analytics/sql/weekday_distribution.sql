SELECT
    EXTRACT(DOW FROM order_date) AS day_of_week_number,
    TO_CHAR(order_date, 'Day') AS day_name,
    COUNT(*) AS orders_count,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_order_value
FROM orders
GROUP BY EXTRACT(DOW FROM order_date), TO_CHAR(order_date, 'Day')
ORDER BY day_of_week_number;
