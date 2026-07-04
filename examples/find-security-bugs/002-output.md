1. **Summary**:
Found 1 vulnerability with a severity of **HIGH**.

2. **Vulnerability Table**:
| ID     | Severity | Vulnerability Type | Description                                                                                                                         |
| ------ | -------- | ------------------ | ----------------------------------------------------------------------------------------------------------------------------------- |
| SEC-01 | HIGH     | Path Traversal     | Joining user input path directly allows reading sensitive system files outside `/var/www/uploads` (e.g., using `../../etc/passwd`). |

3. **Remediation**:
Resolve and validate that the output path stays within the base directory:
```python
import os

def load_file(user_path):
    base_dir = os.path.abspath("/var/www/uploads")
    full_path = os.path.abspath(os.path.join(base_dir, user_path))
    if not full_path.startswith(base_dir):
        raise ValueError("Access Denied")
    with open(full_path, "r") as f:
        return f.read()
```
