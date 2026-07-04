def test_add_happy_path():
    # Arrange, Act, Assert
    x, y = 1, 2
    res = add(x, y)
    assert res == 3

def test_add_negative_numbers():
    assert add(-1, -1) == -2

def test_add_zero():
    assert add(0, 5) == 5