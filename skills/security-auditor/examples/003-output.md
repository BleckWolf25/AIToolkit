<audit_report>
<vulnerability severity="CRITICAL">
  <location>Line 2</location>
  <type>Plaintext Comparison (CWE-328)</type>
  <exploit_scenario>Timing attacks and cleartext validation vulnerabilities.</exploit_scenario>
  <remediation_code><![CDATA[
import bcrypt
return bcrypt.checkpw(pwd.encode(), hash.encode())
]]></remediation_code>
</vulnerability>
</audit_report>
<audit_status>VULNERABLE</audit_status>