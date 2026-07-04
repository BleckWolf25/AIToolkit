1. **Overview**:
Generated a `UserClient` class in Python using `requests` with a `get_user` method matching the `/users/{id}` path.

2. **Client Implementation**:
```python
import requests

class UserClient:
    def __init__(self, base_url="https://api.example.com"):
        self.base_url = base_url.rstrip("/")

    def get_user(self, user_id: int) -> dict:
        url = f"{self.base_url}/users/{user_id}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
```

3. **Usage Example**:
```python
client = UserClient()
user = client.get_user(123)
print(user)
```
