def get_user_data(user_id):
    return db.query("SELECT * FROM users WHERE id = " + user_id)