#!/usr/bin/env python3
"""
__file__ = "runner.py"
__version__ = "1.0.0"
__author__ = "BleckWolf25"
__license__ = "MIT"
__date__ = "03/07/2026"
__updated__ = "04/07/2026"

Loads a prompt template + its sidecar config, renders it against one or
more example inputs, sends it to the configured LLM API, and checks the
output against the assertions defined in a .cases.yaml file.

Usage:
    python tests/runner.py --case tests/cases/refactor-logic.cases.yaml

Requires an LLM_API_KEY environment variable. This script is provider
agnostic in structure; wire up the `call_llm` function to whichever API
you use (OpenAI, Anthropic, Gemini, etc).
"""
# ---------- IMPORTS
import argparse
import os
import re
import sys

from pathlib import Path
from typing import Any

import json
import yaml
import litellm
import assertions

# ---------- CONSTANTS
sys.path.insert(0, str(Path(__file__).resolve().parent))
REPO_ROOT = Path(__file__).resolve().parent.parent

# ---------- FUNCTIONS
def load_yaml(path: Path) -> dict:
    """Load a YAML file into a dictionary."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def render_template(template_text: str, variables: dict) -> str:
    """Render a template string by substituting {{VARIABLE}} placeholders."""
    rendered = template_text
    for key, value in variables.items():
        rendered = rendered.replace("{{" + key + "}}", str(value))
    remaining = re.findall(r"{{(.*?)}}", rendered)
    if remaining:
        raise ValueError(f"Unfilled template variables: {remaining}")
    return rendered


def load_few_shot_examples(config_dir: Path, examples_rel_path: str) -> list:
    """Load alternating user and assistant messages from the examples directory."""
    messages = []
    if not examples_rel_path:
        return messages

    examples_dir = (config_dir / examples_rel_path).resolve()
    if not examples_dir.exists() or not examples_dir.is_dir():
        return messages

    # Gather inputs and outputs
    inputs = {}
    outputs = {}
    for path in examples_dir.iterdir():
        if not path.is_file():
            continue
        # Match pattern: {number}-input.{ext}
        match_in = re.match(r"^(\d+)-input\.", path.name)
        if match_in:
            idx = int(match_in.group(1))
            inputs[idx] = path

        # Match pattern: {number}-output.{ext}
        match_out = re.match(r"^(\d+)-output\.", path.name)
        if match_out:
            idx = int(match_out.group(1))
            outputs[idx] = path

    # Pair them up in order
    sorted_indices = sorted(list(set(inputs.keys()) & set(outputs.keys())))
    for idx in sorted_indices:
        in_content = inputs[idx].read_text(encoding="utf-8")
        out_content = outputs[idx].read_text(encoding="utf-8")
        messages.append({"role": "user", "content": in_content})
        messages.append({"role": "assistant", "content": out_content})

    return messages


def call_llm(
    system_prompt: str, user_input: str, config: dict, few_shot_messages: list | None = None
) -> str:
    """Call LLM using litellm with system, user prompts, and few-shot context."""
    api_key = os.environ.get("LLM_API_KEY")
    if not api_key:
        raise EnvironmentError("LLM_API_KEY is not set")

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    if few_shot_messages:
        messages.extend(few_shot_messages)

    if user_input:
        messages.append({"role": "user", "content": user_input})

    if not messages:
        messages.append({"role": "user", "content": " "})

    response: Any = litellm.completion(
        model=config.get("target_model", "gpt-4o"),
        messages=messages,
        temperature=config.get("temperature", 0.0),
        api_key=api_key
    )

    choices = getattr(response, "choices", None)
    if choices and len(choices) > 0:
        return str(getattr(choices[0].message, "content", "") or "")
    return ""


def run_case_file(case_path: Path) -> bool:
    """Run all evaluation cases defined in a .cases.yaml file."""
    cases = load_yaml(case_path)
    prompt_config_path = REPO_ROOT / cases["prompt_config"]
    prompt_config = load_yaml(prompt_config_path)

    system_prompt_path = prompt_config_path.parent / prompt_config["system_prompt"]
    template_text = system_prompt_path.read_text(encoding="utf-8")

    # Load few-shot examples if examples_dir is present
    examples_rel_path = prompt_config.get("examples_dir")
    few_shot_messages = []
    if examples_rel_path:
        few_shot_messages = load_few_shot_examples(prompt_config_path.parent, examples_rel_path)

    all_passed = True
    for case in cases["cases"]:
        rendered = render_template(template_text, case["variables"])
        # Pass the rendered template as the user_input instead of system_prompt,
        # or use system_prompt depending on preferences.
        try:
            output = call_llm("", rendered, prompt_config, few_shot_messages)
        except NotImplementedError as e:
            print(f"  [SKIP] {case['name']}: {e}")
            continue

        passed = True
        for assertion in case.get("assertions", []):
            if assertion == "is_valid_json":
                if not assertions.is_valid_json(output):
                    passed = False
                    print(f"  [FAIL] {case['name']}: output is not valid JSON")
            elif assertion.startswith("contains_headers:"):
                headers = [h.strip() for h in assertion.split("contains_headers:", 1)[1].split(",")]
                if not assertions.contains_headers(output, headers):
                    passed = False
                    print(f"  [FAIL] {case['name']}: missing expected headers {headers}")
            elif assertion.startswith("contains:"):
                needle = assertion.split("contains:", 1)[1].strip()
                if needle not in output:
                    passed = False
                    print(f"  [FAIL] {case['name']}: missing expected text '{needle}'")
            elif assertion.startswith("matches_schema:"):
                schema_rel = assertion.split("matches_schema:", 1)[1].strip()
                schema_path = (REPO_ROOT / schema_rel).resolve()
                if not schema_path.exists():
                    schema_path = (case_path.parent / schema_rel).resolve()

                if not schema_path.exists():
                    passed = False
                    print(f"  [FAIL] {case['name']}: schema file not found at {schema_rel}")
                    continue

                try:
                    with open(schema_path, "r", encoding="utf-8") as sf:
                        schema_data = json.load(sf)
                except (OSError, ValueError, json.JSONDecodeError) as e:
                    passed = False
                    print(f"  [FAIL] {case['name']}: failed to load JSON schema {schema_rel}: {e}")
                    continue

                if not assertions.matches_json_schema(output, schema_data):
                    passed = False
                    print(
                        f"  [FAIL] {case['name']}: output does not match schema {schema_path.name}"
                    )

        if passed:
            print(f"  [PASS] {case['name']}")
        all_passed = all_passed and passed

    return all_passed

# ---------- MAIN
def main():
    """Parse CLI arguments and run the specified test cases."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", required=True, help="Path to a .cases.yaml file")
    args = parser.parse_args()

    ok = run_case_file(Path(args.case))
    sys.exit(0 if ok else 1)

# ---------- ENTRY POINT
if __name__ == "__main__":
    main()
