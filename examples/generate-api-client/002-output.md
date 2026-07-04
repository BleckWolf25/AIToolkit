1. **Overview**:
Generated a `StatusClient` class in JavaScript using `fetch` with a `ping` method.

2. **Client Implementation**:
```javascript
class StatusClient {
  constructor(baseUrl = 'https://api.example.com') {
    this.baseUrl = baseUrl.replace(/\/$/, '');
  }

  async ping() {
    const response = await fetch(`${this.baseUrl}/ping`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  }
}
```

3. **Usage Example**:
```javascript
const client = new StatusClient();
client.ping().then(console.log).catch(console.error);
```
