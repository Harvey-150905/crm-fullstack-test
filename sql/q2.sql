SELECT
    sh.id,
    sh.name,
    ROUND(
        100.0 * SUM(CASE WHEN s.refunded THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS refund_percentage
FROM sale s
JOIN shop sh ON sh.id = s.shop_id
GROUP BY sh.id, sh.name
HAVING COUNT(*) >= 50
ORDER BY refund_percentage DESC, sh.id;