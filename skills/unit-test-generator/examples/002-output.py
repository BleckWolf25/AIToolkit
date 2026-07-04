import pytest

def test_divide_happy_path():
    assert divide(6, 2) == 3.0

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(5, 0)