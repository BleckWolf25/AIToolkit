import sqlite3
def find_user(name):
    conn = sqlite3.connect('db.db')
    return conn.execute(f"SELECT * FROM users WHERE name='{name}'")