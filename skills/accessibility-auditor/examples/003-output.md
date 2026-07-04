<audit_report>
<violation criteria="WCAG 3.3.2 Labels or Instructions">
  <element>&lt;input id="username"&gt;</element>
  <severity>MAJOR</severity>
  <explanation>Input field lacks associated label element.</explanation>
  <remediation><![CDATA[
<label for="username">Username</label>
<input id="username">
]]></remediation>
</violation>
</audit_report>
<compliance_status>NON-COMPLIANT</compliance_status>