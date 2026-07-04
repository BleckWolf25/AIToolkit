import os

def load_file(user_path):
    full_path = os.path.join("/var/www/uploads", user_path)
    with open(full_path, "r") as f:
        return f.read()
