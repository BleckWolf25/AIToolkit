def get_active_users(users):
    result = []
    for u in users:
        if u["active"] == True:
            result.append(u)
    return result

def get_active_user_names(users):
    names = []
    for u in get_active_users(users):
        names.append(u["name"])
    return names