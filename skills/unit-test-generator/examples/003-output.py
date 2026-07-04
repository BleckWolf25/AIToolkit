def test_get_first_non_empty():
    assert get_first([1, 2]) == 1

def test_get_first_empty():
    assert get_first([]) is None