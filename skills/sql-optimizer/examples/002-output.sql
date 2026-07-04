-- Optimized query using INNER JOIN
SELECT orders.* FROM orders
INNER JOIN users ON orders.user_id = users.id
WHERE users.status = 'active';