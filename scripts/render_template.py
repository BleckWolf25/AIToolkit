#!/usr/bin/env python3
"""
__file__ = "render_template.py"
__version__ = "1.0.0"
__author__ = "BleckWolf25"
__license__ = "MIT"
__date__ = "03/07/2026"
__updated__ = "04/07/2026"

Render a {{VARIABLE}} prompt template from the command line.

Usage:
    python scripts/render_template.py prompts/refactor-logic.md \
        --LANGUAGE Python --FRAMEWORK FastAPI --GOAL "execution speed" \
        --RAW_CODE "$(cat some_file.py)"

Unknown --KEY value pairs are treated as template variables. Any
{{VARIABLE}} left unfilled after substitution raises an error.
"""
# ---------- IMPORTS
import argparse
import re
import sys
from pathlib import Path

# ---------- FUNCTIONS
def parse_dynamic_args(argv):
    """Parse dynamic arguments into a dictionary of variables."""
    variables = {}
    key = None
    for arg in argv:
        if arg.startswith("--"):
            key = arg[2:]
            variables[key] = ""
        elif key is not None:
            if variables[key]:
                variables[key] += " " + arg
            else:
                variables[key] = arg
    return variables

# ---------- MAIN
def main():
    """Parse arguments and render the template."""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("template", help="Path to the .md prompt template")
    known, unknown = parser.parse_known_args()

    template_path = Path(known.template)
    if not template_path.exists():
        print(f"Template not found: {template_path}", file=sys.stderr)
        sys.exit(1)

    variables = parse_dynamic_args(unknown)
    text = template_path.read_text(encoding="utf-8")

    for k, v in variables.items():
        text = text.replace("{{" + k + "}}", v)

    remaining = re.findall(r"{{(.*?)}}", text)
    if remaining:
        print(f"Warning: unfilled variables: {remaining}", file=sys.stderr)

    print(text)

# ---------- ENTRY POINT
if __name__ == "__main__":
    main()
