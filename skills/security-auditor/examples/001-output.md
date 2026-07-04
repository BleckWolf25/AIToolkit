<audit_report>
<vulnerability severity="CRITICAL">
  <location>Line 4</location>
  <type>SQL Injection (CWE-89)</type>
  <exploit_scenario>An attacker can input `' OR '1'='1` to bypass constraints.</exploit_scenario>
  <remediation_code><![CDATA[
conn.execute("SELECT * FROM users WHERE name=?", (name,))
]]></remediation_code>
</vulnerability>
</audit_report>
<audit_status>VULNERABLE</audit_status>