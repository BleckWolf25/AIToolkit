<inferred_schema>
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(50) UNIQUE,
  role_id INT,
  session_token VARCHAR(255)
);
</inferred_schema>
<reproduction_steps>
1. Create users database schema.
2. Implement auth token verification endpoint.
</reproduction_steps>