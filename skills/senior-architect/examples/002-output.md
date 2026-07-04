<thought_process>
1. Heavy export tasks exhaust resources needed for billing/auth.
</thought_process>
<architectural_critique>
- **Scalability Concerns:** Resource starvation on shared server during file exports.
</architectural_critique>
<proposed_architecture><![CDATA[
Decouple file exports into an asynchronous queue (e.g. BullMQ / SQS) handled by a separate worker pool.
]]></proposed_architecture>