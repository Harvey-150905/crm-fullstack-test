SELECT
    c.id,
    c.email
FROM customer c
WHERE EXISTS (
    SELECT 1
    FROM sale s
    WHERE s.customer_id = c.id
      AND s.created_at >= NOW() - INTERVAL '120 days'
      AND s.created_at <  NOW() - INTERVAL '60 days'
)
AND NOT EXISTS (
    SELECT 1
    FROM sale s
    WHERE s.customer_id = c.id
      AND s.created_at >= NOW() - INTERVAL '60 days'
);