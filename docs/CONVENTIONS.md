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

## LLM Generation Parameters

In addition to temperature, config files should define other hyper-parameters depending on the task requirements:

### Temperature & Top-P

- **`temperature`**: Controls randomness. Use lower values for structure/factuality, higher for creativity.
- **`top_p`**: Nucleus sampling. Restricts token selection to the cumulative probability mass.
  - *Rule of thumb:* Modify either `temperature` or `top_p`, but not both (if unsure, default `top_p` to `1.0`).

| Use case                                     | Temperature | Top-P  |
| -------------------------------------------- | ----------- | ------ |
| Code debugging, data parsing, SQL generation | `0.0`       | `1.0`  |
| Structured summarization, analysis           | `0.1 - 0.3` | `0.9`  |
| General Q&A, chat assistants                 | `0.3 - 0.5` | `0.9`  |
| Brainstorming, creative writing, roleplay    | `0.7+`      | `0.95` |

### Token Limits & Penalty Settings

- **`max_tokens`**: Always specify to prevent runaway generation or early truncation.
  - Simple answers/data parsing: `500 - 1000`
  - Complex refactoring or test generation: `2000 - 4000`
- **`presence_penalty` / `frequency_penalty`**: range `[-2.0, 2.0]`.
  - Positive values penalize repeating words/tokens. Use `0.1 - 0.5` in summarization/reviews to force varied terminology.

### Reasoning & Thinking Budgets

For reasoning/CoT models (such as OpenAI `o1`/`o3-mini` or Gemini Thinking models):
- **`thinking` / `reasoning_effort`**:
  - Set `reasoning_effort` (`low`, `medium`, `high`) or `thinking: true` to configure the duration and depth of pre-completion thinking.
  - Set higher reasoning effort for logic, math, structural validation, and architectural planning.

## Variables

Use `{{UPPER_SNAKE_CASE}}` for template variables. List every variable used
in the `.md` file inside the sidecar config's `variables:` array, CI checks
that these stay in sync.

## Verification

Update `last_verified` in a prompt's config whenever you confirm it still
behaves correctly against its `target_model`. Stale (>90 day) prompts should
be re-verified before being trusted in production workflows.

