<red_team_report>
<risk category="OPERATIONAL">
  <description>Write locks on user sessions will cause service timeouts.</description>
  <implication>Users will face errors, resulting in high support ticket volume.</implication>
  <validation_test>Measure query block time on locked sandbox tables.</validation_test>
</risk>
</red_team_report>