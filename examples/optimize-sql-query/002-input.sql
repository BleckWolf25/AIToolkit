-- SCHEMA
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    name VARCHAR(100),
    category_id INT
);
CREATE TABLE sales (
    sale_id INT PRIMARY KEY,
    product_id INT,
    amount DECIMAL(10,2)
);

-- TARGET QUERY
SELECT p.name, SUM(s.amount) 
FROM products p 
JOIN sales s ON p.product_id = s.product_id 
GROUP BY p.name;
