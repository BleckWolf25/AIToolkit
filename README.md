# AI Prompt Engineering Toolkit

A structured, version-controlled environment for AI skills, prompts, few-shot
examples, and automated evaluation, not just a folder of text files.

## Overview

This toolkit provides a systematic way to develop, version, and evaluate LLM prompts across multiple providers. By separating prompts, configurations, and few-shot examples, you can avoid regressions when upgrading models and maintain clean, manageable codebases.

### Architecture

```
skills/     Persona-level system instructions (long-lived identities)
prompts/    Task-level, reusable templates with {{VARIABLES}}
examples/   Golden input/output pairs used for few-shot anchoring and eval
context/    Reference schemas/docs ("Context Kitchen") kept out of prompts
tests/      Runner + assertions that validate prompt output programmatically
scripts/    CLI helpers (template rendering, scaffolding new prompts)
docs/       Conventions and model-compatibility notes
```

## Features & Components

This repository is designed to be modular. While it includes a full evaluation suite, **you do not need to use the Python tooling to benefit from the repository**. Many users use this toolkit purely as a library of pre-built personas, skills, and prompts.

Here is a breakdown of the core features, what they require, where to find them, and how they interact:

### 1. Personas & Skills (Standalone)
- **Where:** `skills/` directory (e.g., `code-reviewer`, `data-parser`).
- **What it is:** Long-lived system instructions that give an LLM a specific identity, tone, and set of rules.
- **Requirements:** None. These are pure markdown text files.
- **Compatibility:** Can be copy-pasted into any LLM web interface (ChatGPT, Claude, Gemini) or loaded into your own applications as system prompts. They are entirely independent of the Python testing suite.

### 2. Task Prompts & Templates (Standalone)
- **Where:** `prompts/` directory (e.g., `refactor-logic.md`).
- **What it is:** Reusable, task-specific templates with `{{VARIABLE}}` placeholders.
- **Requirements:** None (pure text), though the `scripts/render_template.py` helper is useful for dynamically injecting variables.
- **Compatibility:** Works seamlessly with the Personas above. You typically use a Skill as the "System Prompt" and a Task Prompt as the "User Prompt".

### 3. Examples & Context (Standalone)
- **Where:** `examples/` and `context/` directories.
- **What it is:** `examples/` contains "golden" input/output pairs for few-shot prompting. `context/` contains reference material (JSON schemas, API docs) to keep prompts clean and legible.
- **Requirements:** None.
- **Compatibility:** Used to supplement Prompts and Skills to massively improve model reliability.

### 4. Automated Evaluation Suite (Tooling)
- **Where:** `tests/` and `scripts/` directories.
- **What it is:** A Python-based runner that takes your prompts, injects variables, sends them to major LLMs via `litellm`, and asserts that the output matches expectations.
- **Requirements:** Python, `litellm`, `PyYAML`, and an API Key (e.g., `LLM_API_KEY`).
- **Compatibility:** This feature actively tests the items in `prompts/` and `examples/`. It is strictly optional for users who just want to borrow the markdown files.

## Setup

The toolkit relies on Python and uses `litellm` to dynamically switch between major LLM providers (OpenAI, Anthropic, Google Gemini, etc.) without requiring specific SDK lock-in.

1. **Create and Activate a Virtual Environment:**
   Due to PEP-668 protections on system Python environments, create a local virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure the Environment:**
   Set the API key for your chosen model provider. For instance:
   ```bash
   export LLM_API_KEY="your-api-key-here"
   # Depending on the model, litellm will natively pick up provider-specific keys like OPENAI_API_KEY as well.
   ```

## Usage

### 1. Scaffolding a New Prompt
Use the included python script to quickly scaffold a new prompt template, configuration file, and placeholder examples:

```bash
python scripts/new_prompt.py my-new-prompt
```
This generates `prompts/my-new-prompt.md`, `prompts/my-new-prompt.config.yaml`, and initial examples.

### 2. Rendering Templates
You can dynamically render a prompt for manual inspection or injection into other workflows:

```bash
python scripts/render_template.py prompts/refactor-logic.md --LANGUAGE Python --FRAMEWORK FastAPI --GOAL "execution speed"
```
Unknown arguments are treated as template variables mapping directly to `{{VARIABLES}}`.

### 3. Evaluating Prompts
To test for regressions or changes in model outputs, run the evaluation suite against a defined test case file:

```bash
python tests/runner.py --case tests/cases/refactor-logic.cases.yaml
```
The runner will dynamically call the LLM and run assertions against the outputs using the logic defined in `tests/assertions.py`.

## Conventions & Rules

Every prompt must have two sidecar files:

1. `prompts/<name>.md`, the actual template, using `{{VARIABLE}}` placeholders.
2. `prompts/<name>.config.yaml`, the exact engine settings (temperature, target model, allowed variables), and links to its example pairs and eval cases.

See [docs/CONVENTIONS.md](docs/CONVENTIONS.md) for naming and versioning rules, and [docs/MODEL_COMPAT.md](docs/MODEL_COMPAT.md) for verification details against model versions.

## Why this structure?

- **Parameter Configs:** Attaches exact engine settings (temperature, target model) directly to the prompt.
- **Few-shot Pairs:** Examples provide the fastest way to re-anchor a prompt when an upstream model silently changes behavior.
- **Templating:** Turns single-use prompts into scalable, reusable assets.
- **Tests & CI:** Migrates prompt regressions from "bugs found in production" to "failing tests caught in CI".
- **Context Kitchen:** Keeps large reference materials isolated, ensuring core prompt instructions remain short and legible.

## Contributing

Open a PR using the template, it will ask you to confirm you've added or updated an example pair and run the eval suite locally. See [CODEOWNERS](.github/CODEOWNERS) for review routing.
