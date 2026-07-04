def get_discount(price, is_member):
    if is_member:
        return price * 0.9
    else:
        return price