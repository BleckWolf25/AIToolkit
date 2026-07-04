1. **Optimization Analysis**:
The query currently requires a full table scan on the `orders` table because there are no indexes on `customer_id` or `status`.

2. **Optimized Query**:
```sql
SELECT order_id, customer_id, order_date, status, total_amount 
FROM orders 
WHERE customer_id = 999 AND status = 'COMPLETED';
```

3. **Recommended Index**:
```sql
CREATE INDEX idx_orders_customer_status ON orders(customer_id, status);
```

4. **Estimated Costs Comparison**:
| Approach | Scan Method | Time Complexity |
|---|---|---|
| Original | Full Table Scan | O(N) |
| Optimized | Index Scan | O(log N) |
