1. [MEDIUM] `u["active"] == True` is a redundant comparison; `if u["active"]`
   is equivalent and avoids an extra boolean comparison per iteration.
2. [MEDIUM] `get_active_user_names` iterates `get_active_users(users)`, which
   itself iterates `users`, two full passes and one intermediate list
   allocation where one pass would do.
3. [LOW] Both functions use manual accumulation loops where a list
   comprehension is more idiomatic and marginally faster in CPython.

```python
def get_active_users(users):
    return [u for u in users if u["active"]]

def get_active_user_names(users):
    return [u["name"] for u in users if u["active"]]
```

Trade-offs: `get_active_user_names` no longer reuses `get_active_users`,
duplicating the filter condition in two places, acceptable here for the
single-pass performance win, but worth a comment if the condition grows
more complex.
