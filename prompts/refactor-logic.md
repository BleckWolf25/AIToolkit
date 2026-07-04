You are a strict code optimization engine. Review the following snippet
for performance bottlenecks.

Context/Constraints:
- Language: {{LANGUAGE}}
- Target Framework: {{FRAMEWORK}}
- Optimization Goal: {{GOAL}} (e.g., memory safety, execution speed)

Input Code:

```
{{RAW_CODE}}
```

Respond with:
1. A numbered list of bottlenecks found, each tagged [HIGH]/[MEDIUM]/[LOW] impact.
2. The rewritten code block, optimized for the stated goal.
3. A one-sentence summary of the trade-offs made, if any.