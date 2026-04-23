-- Antes: ejecución sin índice optimizado
EXPLAIN (ANALYZE, BUFFERS)
SELECT s.id, sh.name, p.name, si.qty
FROM sale s
JOIN shop sh ON sh.id = s.shop_id
JOIN saleitem si ON si.sale_id = s.id
JOIN product p ON p.id = si.product_id
WHERE s.created_at >= NOW() - INTERVAL '30 days'
AND sh.name ILIKE '%central%'
ORDER BY s.created_at DESC
LIMIT 100;

-- Problema:
-- ILIKE '%central%' no puede usar un índice B-tree porque el patrón empieza con wildcard (%).
-- Esto obliga a PostgreSQL a hacer un Seq Scan (escaneo completo de la tabla).

-- Solución:
-- Se utiliza la extensión pg_trgm con un índice GIN para permitir búsquedas eficientes por similitud.

CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE INDEX idx_shop_name_trgm
ON shop USING GIN (name gin_trgm_ops);

-- Después: ejecución con índice GIN
EXPLAIN (ANALYZE, BUFFERS)
SELECT s.id, sh.name, p.name, si.qty
FROM sale s
JOIN shop sh ON sh.id = s.shop_id
JOIN saleitem si ON si.sale_id = s.id
JOIN product p ON p.id = si.product_id
WHERE s.created_at >= NOW() - INTERVAL '30 days'
AND sh.name ILIKE '%central%'
ORDER BY s.created_at DESC
LIMIT 100;

-- Resultado esperado:
-- Antes: Seq Scan sobre shop
-- Después: Bitmap Index Scan o Index Scan
-- Mejora significativa en tiempo de ejecución