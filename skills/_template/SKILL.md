# Skill Name

## Persona

Describe who this AI is acting as, in 2-4 sentences. This is the identity that persists across every task the skill is used for. You can inject `{{VARIABLES}}` here to make the persona adaptable (e.g., "You are an expert in {{DOMAIN}}.").

## Scope

- **IS for:** What this skill is designed to handle (e.g., parsing, reviewing, writing).
- **NOT for:** Explicit boundaries of what the skill must never do.

## System Instructions

```
<Paste the exact system prompt text here. This is what goes in the "system" role of the API call, separate from any per-task user input.>

### Core Directives:
1. Directive one.
2. Directive two.

### Context:
<Use {{VARIABLE_NAME}} placeholders here to inject dynamic requirements from the config.yaml file>

### Output Format:
<Explicitly define how the AI should structure its output, ideally using XML tags like <thought_process> and <final_result> to ensure reasoning before answering.>
```

## Notes

Anything else a future maintainer needs to know: known failure modes, edge cases, or model-specific quirks. Remember to list all `{{VARIABLES}}` used in this file inside the `config.yaml`'s `variables:` array.