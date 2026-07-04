#!/usr/bin/env python3
"""
__file__ = "new_prompt.py"
__version__ = "1.0.0"
__author__ = "BleckWolf25"
__license__ = "MIT"
__date__ = "03/07/2026"
__updated__ = "04/07/2026"

Scaffold a new prompt: creates prompts/<name>.md, prompts/<name>.config.yaml,
and an examples/<name>/ folder with placeholder files.

Usage:
    python scripts/new_prompt.py my-new-prompt
"""
# ---------- IMPORTS
import argparse
import sys
from pathlib import Path
from datetime import date

# ---------- MAIN FUNCTION
def main():
    """Create scaffold files for a new prompt.

    This function parses a single command-line argument (name) and creates
    a markdown prompt, a config yaml, and an examples directory with
    placeholder files. Exits with code 1 if the prompt markdown already
    exists.
    """
    parser = argparse.ArgumentParser(description="Scaffold a new prompt.")
    parser.add_argument("name", help="The name of the new prompt")
    args = parser.parse_args()

    name = args.name
    root_dir = Path(__file__).resolve().parent.parent

    prompt_md = root_dir / "prompts" / f"{name}.md"
    prompt_cfg = root_dir / "prompts" / f"{name}.config.yaml"
    examples_dir = root_dir / "examples" / name

    if prompt_md.exists():
        print(f"Prompt already exists: {prompt_md}", file=sys.stderr)
        sys.exit(1)

    examples_dir.mkdir(parents=True, exist_ok=True)

    prompt_md_content = """You are a [ROLE]. [TASK DESCRIPTION].

Context/Constraints:
- {{{{VARIABLE_ONE}}}}
- {{{{VARIABLE_TWO}}}}

Input:

```
{{{{RAW_INPUT}}}}
```

Respond with: [DESCRIBE EXPECTED OUTPUT FORMAT]
"""
    prompt_md.write_text(prompt_md_content, encoding="utf-8")

    prompt_cfg_content = f"""id: {name}
version: 0.1.0
target_model: gpt-4o
fallback_models: []
temperature: 0.0
max_tokens: 1000
system_prompt: ./{name}.md
variables:
  - VARIABLE_ONE
  - VARIABLE_TWO
  - RAW_INPUT
examples_dir: ../examples/{name}
last_verified: {date.today().strftime('%Y-%m-%d')}
"""
    prompt_cfg.write_text(prompt_cfg_content, encoding="utf-8")

    (examples_dir / "001-input.txt").touch()
    (examples_dir / "001-output.md").touch()

    print("Created:")
    print(f"  {prompt_md.relative_to(root_dir)}")
    print(f"  {prompt_cfg.relative_to(root_dir)}")
    print(f"  {(examples_dir / '001-input.txt').relative_to(root_dir)}")
    print(f"  {(examples_dir / '001-output.md').relative_to(root_dir)}")

# ---------- ENTRY POINT
if __name__ == "__main__":
    main()
