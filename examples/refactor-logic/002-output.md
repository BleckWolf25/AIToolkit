1. [LOW] Manual accumulation loop; `sum()` with a generator expression is
   more idiomatic and avoids re-binding `total` on every iteration.

```python
def total_price(items):
    return sum(item["price"] * item["qty"] for item in items)
```

Trade-offs: none meaningful at this scale; readability and performance
both improve.