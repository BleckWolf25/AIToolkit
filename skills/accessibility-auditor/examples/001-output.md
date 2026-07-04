<audit_report>
<violation criteria="WCAG 1.1.1 Non-text Content">
  <element>&lt;img src="logo.png"&gt;</element>
  <severity>CRITICAL</severity>
  <explanation>Missing alt attribute prevents screen readers from announcing image purpose.</explanation>
  <remediation><![CDATA[
<img src="logo.png" alt="Company Logo">
]]></remediation>
</violation>
</audit_report>
<compliance_status>NON-COMPLIANT</compliance_status>