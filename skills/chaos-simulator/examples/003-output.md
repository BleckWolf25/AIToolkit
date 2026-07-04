<failure_scenarios>
- DNS resolution failure: Remote requests timeout.
</failure_scenarios>
<simulation_code>
route add -host api.thirdparty.com reject
</simulation_code>