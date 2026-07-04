1. **Test Strategy**:
I am testing boundary conditions (negative price), VIP discounts (20% off), Member discounts (5% off), and regular customers (no discount).

2. **Test Suite**:
```python
import pytest
from discount_service import calculate_discount

def test_negative_price_raises_error():
    with pytest.raises(ValueError, match="Price cannot be negative"):
        calculate_discount(-10, "VIP")

def test_vip_discount():
    assert calculate_discount(100, "VIP") == 80.0

def test_member_discount():
    assert calculate_discount(100, "Member") == 95.0

def test_regular_customer():
    assert calculate_discount(100, "Regular") == 100.0
```

3. **Checklist**:
- Integration tests checking that user_level is resolved correctly from the database database layer.
- Load/stress tests verifying discount calculations handle bulk order arrays.
