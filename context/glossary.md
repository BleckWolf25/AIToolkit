# Glossary

Shared terminology referenced across multiple prompts/skills, so
definitions live in one place instead of being repeated (and drifting)
inside individual prompt files.

- **Golden example**: an input/output pair known to represent ideal model
  behavior; used both as few-shot anchoring and as an automated test case.
- **Sidecar config**: the `.config.yaml` file that sits next to a prompt or
  skill's markdown file and carries its execution metadata.
- **Re-anchoring**: feeding golden examples back into a degraded prompt
  after a model update to restore expected behavior.
