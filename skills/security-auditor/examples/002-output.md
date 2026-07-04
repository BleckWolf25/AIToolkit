<audit_report>
<vulnerability severity="HIGH">
  <location>Line 3</location>
  <type>Insecure Randomness (CWE-330)</type>
  <exploit_scenario>The `random` module is pseudo-random and predictable.</exploit_scenario>
  <remediation_code><![CDATA[
import secrets
token = secrets.token_hex(16)
]]></remediation_code>
</vulnerability>
</audit_report>
<audit_status>VULNERABLE</audit_status>