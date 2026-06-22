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