-- Recommends composite index on products(created_at)
-- CREATE INDEX idx_products_created_at ON products(created_at);
SELECT * FROM products ORDER BY created_at LIMIT 10;