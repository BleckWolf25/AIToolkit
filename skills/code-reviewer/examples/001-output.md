<thought_process>
1. Mutable default argument detected.
</thought_process>
<review_comments>
<issue severity="BLOCKER">
<location>Line 1</location>
<description>Mutable default argument list creates persistent state between calls.</description>
<proposed_fix><![CDATA[
def append_to(element, to=None):
    if to is None:
        to = []
    to.append(element)
    return to
]]></proposed_fix>
</issue>
</review_comments>
<verdict>REQUEST CHANGES</verdict>