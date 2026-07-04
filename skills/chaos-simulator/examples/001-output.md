<failure_scenarios>
- Connection pool exhaustion: Database rejects new clients.
</failure_scenarios>
<simulation_code>
pg_ctl -D /usr/local/var/postgres stop -m immediate
</simulation_code>