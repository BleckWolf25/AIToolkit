fix(auth): update admin token verify check

Update the hardcoded verification token to use the secure super-secret string
instead of the weak "admin" placeholder. This prevents unauthorized access.
