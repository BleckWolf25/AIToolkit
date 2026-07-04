#!/usr/bin/env python3
"""
__file__ = "playground.py"
__version__ = "1.0.0"
__author__ = "BleckWolf25"
__license__ = "MIT"
__date__ = "04/07/2026"
__updated__ = "04/07/2026"

Interactive Command-Line Playground for AI System Personas and Task Prompts.
Allows developers to select a persona/skill, select a prompt, interactively fill
template variables, inject few-shot examples, and stream responses live from LiteLLM.

Usage:
    # Interactive mode:
    python scripts/playground.py

    # Fast-path CLI mode:
    python scripts/playground.py --skill security-auditor --prompt refactor-logic \
        --var LANGUAGE=Python --var FRAMEWORK=Django --var GOAL=security --var RAW_CODE="test"
"""
# ---------- IMPORTS
import argparse
import os
import re
import sys
from pathlib import Path
from typing import Any
import yaml

try:
    import litellm
except ImportError:
    litellm = None

# ---------- CONSTANTS
REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
PROMPTS_DIR = REPO_ROOT / "prompts"

# ---------- FUNCTIONS
def load_yaml(path: Path) -> dict:
    """Load a YAML file into a dictionary."""
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def render_template(template_text: str, variables: dict) -> str:
    """Render a template string by substituting {{VARIABLE}} placeholders."""
    rendered = template_text
    for key, value in variables.items():
        rendered = rendered.replace("{{" + key + "}}", str(value))
    return rendered


def load_few_shot_examples(config_dir: Path, examples_rel_path: str) -> list:
    """Load alternating user and assistant messages from the examples directory."""
    messages = []
    if not examples_rel_path:
        return messages

    examples_dir = (config_dir / examples_rel_path).resolve()
    if not examples_dir.exists() or not examples_dir.is_dir():
        return messages

    inputs = {}
    outputs = {}
    for path in examples_dir.iterdir():
        if not path.is_file():
            continue
        match_in = re.match(r"^(\d+)-input\.", path.name)
        if match_in:
            idx = int(match_in.group(1))
            inputs[idx] = path

        match_out = re.match(r"^(\d+)-output\.", path.name)
        if match_out:
            idx = int(match_out.group(1))
            outputs[idx] = path

    sorted_indices = sorted(list(set(inputs.keys()) & set(outputs.keys())))
    for idx in sorted_indices:
        in_content = inputs[idx].read_text(encoding="utf-8")
        out_content = outputs[idx].read_text(encoding="utf-8")
        messages.append({"role": "user", "content": in_content})
        messages.append({"role": "assistant", "content": out_content})

    return messages


def discover_skills() -> list:
    """Discover available skills in the skills directory."""
    skills = []
    if SKILLS_DIR.exists():
        for p in sorted(SKILLS_DIR.iterdir()):
            if p.is_dir() and p.name != "_template" and (p / "config.yaml").exists():
                skills.append(p)
    return skills


def discover_prompts() -> list:
    """Discover available task prompts in the prompts directory."""
    prompts = []
    if PROMPTS_DIR.exists():
        for p in sorted(PROMPTS_DIR.glob("*.md")):
            config_file = p.with_suffix("").with_suffix(".config.yaml")
            if config_file.exists():
                prompts.append(p)
    return prompts


def select_from_menu(
    title: str, items: list, allow_none: bool = True, none_label: str = "None"
) -> int:
    """Display an interactive menu and return the selected index (-1 for None)."""
    print(f"\n=== {title} ===")
    start_idx = 0 if allow_none else 1
    if allow_none:
        print(f"  0. [{none_label}]")
    for idx, item in enumerate(items, start=1):
        name = item.name if isinstance(item, Path) else str(item)
        print(f"  {idx}. {name}")

    while True:
        try:
            choice = input(f"\nSelect an option ({start_idx}-{len(items)}): ").strip()
            if not choice:
                continue
            val = int(choice)
            if allow_none and val == 0:
                return -1
            if 1 <= val <= len(items):
                return val - 1
            print("Invalid selection, try again.")
        except (ValueError, EOFError):
            print("Invalid input, please enter a valid number.")


def collect_variables(needed_vars: set, provided_vars: dict) -> dict:
    """Collect required variables from provided CLI args or interactive stdin."""
    result = dict(provided_vars)
    missing = needed_vars - set(result.keys())
    if not missing:
        return result

    print("\n--- Variable Collection ---")
    for var in sorted(missing):
        val = input(f"Enter value for '{{{{{var}}}}}': ").strip()
        result[var] = val
    return result


def stream_response(model: str, messages: list, temperature: float):
    """Call LiteLLM and stream the output to the terminal."""
    if litellm is None:
        print("[ERROR] litellm package is not installed. Please run: pip install litellm")
        sys.exit(1)

    api_key = os.environ.get("LLM_API_KEY")
    if not api_key:
        print("\n[WARNING] LLM_API_KEY environment variable is not set!")
        print("Unless using a local mock/Ollama provider, authentication may fail.\n")

    print(f"\n>>> Sending request to model: {model} (temp: {temperature}) >>>")
    print("--- Assistant Response ---\n")

    try:
        response: Any = litellm.completion(
            model=model,
            messages=messages,
            temperature=temperature,
            stream=True,
            api_key=api_key
        )
        for chunk in response:  # type: ignore[union-attr]
            choices = getattr(chunk, "choices", None)
            if choices and len(choices) > 0:
                delta = getattr(choices[0], "delta", None)
                content = getattr(delta, "content", "") or ""
                print(str(content), end="", flush=True)
        print("\n\n--- End of Response ---")
    except (RuntimeError, ValueError, KeyError, AttributeError, OSError) as e:
        print(f"\n[ERROR] API completion failed: {e}")
        sys.exit(1)


# ---------- MAIN
def main():
    """Parse CLI arguments and launch interactive or fast-path playground execution."""
    parser = argparse.ArgumentParser(description="AI Toolkit Interactive Playground")
    parser.add_argument("--skill", help="Name of the skill/persona directory in skills/")
    parser.add_argument(
        "--prompt", help="Name of the prompt template in prompts/ (without extension)"
    )
    parser.add_argument(
        "--var", action="append", help="Variable override in KEY=VALUE format", default=[]
    )
    parser.add_argument(
        "--model", help="Target LLM model override (default: gpt-4o)", default="gpt-4o"
    )
    parser.add_argument("--temperature", type=float, help="Temperature override", default=0.0)
    args = parser.parse_args()

    # Parse CLI variables
    cli_vars = {}
    for v in args.var:
        if "=" in v:
            k, val = v.split("=", 1)
            cli_vars[k.strip()] = val.strip()

    skills = discover_skills()
    prompts = discover_prompts()

    selected_skill = None
    if args.skill:
        matching = [s for s in skills if s.name == args.skill]
        if not matching:
            print(f"[ERROR] Skill '{args.skill}' not found.")
            sys.exit(1)
        selected_skill = matching[0]
    elif not (args.skill or args.prompt or cli_vars):
        # Interactive mode
        idx = select_from_menu(
            "Choose Persona / Skill",
            skills,
            allow_none=True,
            none_label="No Persona (Standard Chat)",
        )
        if idx >= 0:
            selected_skill = skills[idx]

    selected_prompt = None
    if args.prompt:
        matching = [p for p in prompts if args.prompt in (p.stem, p.name)]
        if not matching:
            print(f"[ERROR] Prompt '{args.prompt}' not found.")
            sys.exit(1)
        selected_prompt = matching[0]
    elif not (args.skill or args.prompt or cli_vars):
        # Interactive mode
        idx = select_from_menu(
            "Choose Task Prompt",
            prompts,
            allow_none=True,
            none_label="Custom Free-Form Input",
        )
        if idx >= 0:
            selected_prompt = prompts[idx]

    # Load configurations
    skill_config = {}
    prompt_config = {}
    needed_vars = set()

    system_text = ""
    if selected_skill:
        skill_config = load_yaml(selected_skill / "config.yaml")
        sys_rel = skill_config.get("system_prompt", "SKILL.md")
        sys_path = (selected_skill / sys_rel).resolve()
        if sys_path.exists():
            system_text = sys_path.read_text(encoding="utf-8")
        needed_vars.update(skill_config.get("variables", []))

    user_text = ""
    if selected_prompt:
        prompt_config = load_yaml(selected_prompt.with_suffix("").with_suffix(".config.yaml"))
        user_text = selected_prompt.read_text(encoding="utf-8")
        needed_vars.update(prompt_config.get("variables", []))
    elif not args.prompt and not (args.skill or cli_vars):
        print("\n--- Free-Form Prompt ---")
        user_text = input("Enter your custom task query: ").strip()

    # Collect variables
    filled_vars = collect_variables(needed_vars, cli_vars)

    # Render messages
    messages = []
    if system_text:
        rendered_sys = render_template(system_text, filled_vars)
        messages.append({"role": "system", "content": rendered_sys})

    # Load few-shot examples (prioritize skill examples, then prompt examples)
    few_shot_msgs = []
    if selected_skill and skill_config.get("examples_dir"):
        few_shot_msgs.extend(load_few_shot_examples(selected_skill, skill_config["examples_dir"]))
    if selected_prompt and prompt_config.get("examples_dir"):
        few_shot_msgs.extend(
            load_few_shot_examples(selected_prompt.parent, prompt_config["examples_dir"])
        )

    if few_shot_msgs:
        messages.extend(few_shot_msgs)

    if user_text:
        rendered_user = render_template(user_text, filled_vars)
        messages.append({"role": "user", "content": rendered_user})

    if not messages:
        print("[ERROR] No prompt content to send to the model.")
        sys.exit(1)

    # Determine model and temperature
    target_model = (
        args.model
        or skill_config.get("target_model")
        or prompt_config.get("target_model")
        or "gpt-4o"
    )
    target_temp = (
        args.temperature
        if args.temperature != 0.0
        else (skill_config.get("temperature", 0.0))
    )

    # Run streaming response
    stream_response(target_model, messages, target_temp)


# ---------- ENTRY POINT
if __name__ == "__main__":
    main()
