#!/usr/bin/env python3
"""
__file__ = "assertions.py"
__version__ = "1.0.0"
__author__ = "BleckWolf25"
__license__ = "MIT"
__date__ = "03/07/2026"
__updated__ = "04/07/2026"

Structural validation for the toolkit repository itself:
- every prompts/*.md has a matching *.config.yaml
- every config.yaml lists variables that actually appear in its template
- config files are valid YAML with required keys

Also exposes small reusable output-assertion helpers used by runner.py.

Usage:
    python tests/assertions.py --validate-structure
"""
# ---------- IMPORTS
import argparse
import re
import sys
from pathlib import Path

import json
import yaml
import jsonschema
from jsonschema.exceptions import ValidationError as JsonSchemaValidationError

# ---------- CONSTANTS
REPO_ROOT = Path(__file__).resolve().parent.parent
REQUIRED_CONFIG_KEYS = {"id", "version", "target_model", "temperature", "system_prompt"}

# ---------- FUNCTIONS
def is_valid_json(text: str) -> bool:
    """Check if the given string is valid JSON."""
    try:
        json.loads(text)
        return True
    except json.JSONDecodeError:
        return False


def contains_headers(text: str, headers: list) -> bool:
    """Check if the text contains all the specified markdown headers."""
    return all(re.search(rf"^#+\s*{re.escape(h)}", text, re.MULTILINE) for h in headers)


def matches_json_schema(text: str, schema: dict) -> bool:
    """Check if the given text is valid JSON and matches the provided JSON schema."""
    try:
        data = json.loads(text)
        jsonschema.validate(instance=data, schema=schema)
        return True
    except (json.JSONDecodeError, JsonSchemaValidationError):
        return False


def validate_structure() -> bool:
    """Validate prompt templates and skills have matching configurations and correct layouts."""
    ok = True

    # 1. Validate Prompts
    prompts_dir = REPO_ROOT / "prompts"
    if prompts_dir.exists():
        for md_file in prompts_dir.glob("*.md"):
            config_file = md_file.with_suffix("").with_suffix(".config.yaml")
            if not config_file.exists():
                print(f"[ERROR] Prompt {md_file.name} has no matching config: {config_file.name}")
                ok = False
                continue

            with open(config_file, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)

            missing_keys = REQUIRED_CONFIG_KEYS - config.keys()
            if missing_keys:
                print(f"[ERROR] Config {config_file.name} missing keys: {missing_keys}")
                ok = False

            template_text = md_file.read_text(encoding="utf-8")
            template_vars = set(re.findall(r"{{(.*?)}}", template_text))
            declared_vars = set(config.get("variables", []))

            if template_vars != declared_vars:
                print(
                    f"[ERROR] Prompt {md_file.name}: template vars {template_vars} "
                    f"do not match declared vars {declared_vars} in {config_file.name}"
                )
                ok = False

    # 2. Validate Skills
    skills_dir = REPO_ROOT / "skills"
    if skills_dir.exists():
        for skill_path in skills_dir.iterdir():
            if not skill_path.is_dir() or skill_path.name == "_template":
                continue

            # Check config.yaml
            config_file = skill_path / "config.yaml"
            if not config_file.exists():
                print(f"[ERROR] Skill '{skill_path.name}' is missing config.yaml")
                ok = False
                continue

            with open(config_file, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)

            missing_keys = REQUIRED_CONFIG_KEYS - config.keys()
            if missing_keys:
                print(f"[ERROR] Skill '{skill_path.name}' config missing keys: {missing_keys}")
                ok = False

            # Check system prompt file
            sys_prompt_rel = config.get("system_prompt")
            if not sys_prompt_rel:
                print(f"[ERROR] Skill '{skill_path.name}' config has no system_prompt path defined")
                ok = False
                continue

            sys_prompt_file = (skill_path / sys_prompt_rel).resolve()
            if not sys_prompt_file.exists():
                print(
                    f"[ERROR] Skill '{skill_path.name}' system prompt file does not exist: "
                    f"{sys_prompt_rel}"
                )
                ok = False
                continue

            # Check variables in system prompt
            prompt_text = sys_prompt_file.read_text(encoding="utf-8")
            prompt_vars = set(re.findall(r"{{(.*?)}}", prompt_text))
            declared_vars = set(config.get("variables", []))

            if prompt_vars != declared_vars:
                print(
                    f"[ERROR] Skill '{skill_path.name}' system prompt: variables {prompt_vars} "
                    f"do not match declared variables {declared_vars} in config.yaml"
                )
                ok = False

            # Check examples
            examples_dir = skill_path / "examples"
            if not examples_dir.exists() or not examples_dir.is_dir():
                print(f"[ERROR] Skill '{skill_path.name}' is missing 'examples/' directory")
                ok = False
                continue

            # Verify at least 3 input and 3 output files, and none are empty
            for i in range(1, 4):
                input_pattern = f"{i:03d}-input.*"
                output_pattern = f"{i:03d}-output.*"

                inputs = list(examples_dir.glob(input_pattern))
                outputs = list(examples_dir.glob(output_pattern))

                if not inputs:
                    print(f"[ERROR] Skill '{skill_path.name}' missing example input index {i:03d}")
                    ok = False
                else:
                    for inp in inputs:
                        if inp.stat().st_size == 0:
                            print(
                                f"[ERROR] Skill '{skill_path.name}' example input {inp.name} "
                                f"is empty"
                            )
                            ok = False

                if not outputs:
                    print(f"[ERROR] Skill '{skill_path.name}' missing example output index {i:03d}")
                    ok = False
                else:
                    for out in outputs:
                        if out.stat().st_size == 0:
                            print(
                                f"[ERROR] Skill '{skill_path.name}' example output {out.name} "
                                f"is empty"
                            )
                            ok = False

    return ok

# ---------- MAIN
def main():
    """Parse CLI arguments and run structural validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate-structure", action="store_true")
    args = parser.parse_args()

    if args.validate_structure:
        ok = validate_structure()
        if ok:
            print("Structure validation passed.")
        sys.exit(0 if ok else 1)

# ---------- ENTRY POINT
if __name__ == "__main__":
    main()
