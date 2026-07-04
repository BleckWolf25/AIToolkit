<thought_process>
1. SQL injection vulnerability detected.
</thought_process>
<review_comments>
<issue severity="BLOCKER">
<location>Line 2</location>
<description>Raw string concatenation leads to SQL Injection.</description>
<proposed_fix><![CDATA[
def get_user_data(user_id):
    return db.query("SELECT * FROM users WHERE id = :id", {"id": user_id})
]]></proposed_fix>
</issue>
</review_comments>
<verdict>REQUEST CHANGES</verdict>