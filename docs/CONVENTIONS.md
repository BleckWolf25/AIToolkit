# Conventions

## Naming

- Prompt files: `kebab-case.md` describing the task, not the model
  (e.g. `refactor-logic.md`, not `gpt4-refactor.md`).
- Sidecar config: same basename, `.config.yaml`.
- Skills: one folder per skill under `skills/<skill-name>/`, containing
  `SKILL.md` and `config.yaml`.

## Versioning

Each prompt/skill config carries its own `version` field (semver):

- **Patch** (`1.0.1`): wording tweak, no behavior change.
- **Minor** (`1.1.0`): new variable, expanded scope, still backward compatible.
- **Major** (`2.0.0`): output format changed, breaking downstream consumers.

## Temperature guidelines

| Use case                                 | Temperature |
| ---------------------------------------- | ----------- |
| Code debugging, data parsing, extraction | `0.0`       |
| Structured summarization                 | `0.1 - 0.3` |
| General Q&A                              | `0.3 - 0.5` |
| Brainstorming, creative writing          | `0.7+`      |

## Variables

Use `{{UPPER_SNAKE_CASE}}` for template variables. List every variable used
in the `.md` file inside the sidecar config's `variables:` array, CI checks
that these stay in sync.

## Verification

Update `last_verified` in a prompt's config whenever you confirm it still
behaves correctly against its `target_model`. Stale (>90 day) prompts should
be re-verified before being trusted in production workflows.
