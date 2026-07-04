def double_even_numbers(numbers):
    res = []
    for n in numbers:
        if n % 2 == 0:
            res.append(n * 2)
    return res