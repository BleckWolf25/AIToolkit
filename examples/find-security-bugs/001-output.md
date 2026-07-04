1. **Summary**:
Found 1 vulnerability with a severity of **HIGH**.

2. **Vulnerability Table**:
| ID     | Severity | Vulnerability Type | Description                                                                             |
| ------ | -------- | ------------------ | --------------------------------------------------------------------------------------- |
| SEC-01 | HIGH     | SQL Injection      | Direct string formatting in `cursor.execute()` permits arbitrary SQL payload execution. |

3. **Remediation**:
Use parameterized queries instead of f-strings:
```python
def get_user_data(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name = ?", (username,))
    return cursor.fetchall()
```
