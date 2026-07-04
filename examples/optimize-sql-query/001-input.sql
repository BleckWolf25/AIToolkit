-- SCHEMA
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    status VARCHAR(50),
    total_amount DECIMAL(10,2)
);

-- TARGET QUERY
SELECT * FROM orders WHERE customer_id = 999 AND status = 'COMPLETED';
