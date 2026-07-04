def calculate_discount(price, user_level):
    if price < 0:
        raise ValueError("Price cannot be negative")
    if user_level == "VIP":
        return price * 0.8
    elif user_level == "Member":
        return price * 0.95
    return price
