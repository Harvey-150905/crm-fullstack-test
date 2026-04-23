WITH monthly_product_sales AS (
    SELECT
        TO_CHAR(DATE_TRUNC('month', s.created_at), 'YYYY-MM') AS year_month,
        p.sku,
        p.name,
        SUM(si.qty * si.unit_price_cents) / 100.0 AS revenue_eur,
        SUM(si.qty) AS qty
    FROM sale s
    JOIN saleitem si ON si.sale_id = s.id
    JOIN product p ON p.id = si.product_id
    WHERE s.created_at >= DATE_TRUNC('month', NOW()) - INTERVAL '11 months'
      AND s.refunded = FALSE
    GROUP BY DATE_TRUNC('month', s.created_at), p.sku, p.name
),
ranked AS (
    SELECT
        year_month,
        sku,
        name,
        ROUND(revenue_eur, 2) AS revenue_eur,
        qty,
        ROW_NUMBER() OVER (
            PARTITION BY year_month
            ORDER BY revenue_eur DESC, qty DESC, sku
        ) AS rn
    FROM monthly_product_sales
)
SELECT
    year_month,
    sku,
    name,
    revenue_eur,
    qty
FROM ranked
WHERE rn = 1
ORDER BY year_month;