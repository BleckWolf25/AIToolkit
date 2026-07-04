<audit_report>
<violation criteria="WCAG 2.1.1 Keyboard">
  <element>&lt;div onclick="submit()"&gt;</element>
  <severity>MAJOR</severity>
  <explanation>Interactive elements must be keyboard focusable.</explanation>
  <remediation><![CDATA[
<button onclick="submit()">Submit</button>
]]></remediation>
</violation>
</audit_report>
<compliance_status>NON-COMPLIANT</compliance_status>