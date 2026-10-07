#!/usr/bin/env python3
"""Convert a YAML jobspec to JSON without changing its structure.

Requires PyYAML: python3 -m pip install PyYAML
"""

import argparse
import json
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="YAML jobspec path, or - for stdin")
    parser.add_argument("-o", "--output", help="JSON output path (default: stdout)")
    args = parser.parse_args()

    try:
        import yaml
    except ImportError:
        parser.exit(1, "Install PyYAML with: python3 -m pip install PyYAML\n")

    try:
        source = sys.stdin.read() if args.input == "-" else Path(args.input).read_text(encoding="utf-8")
        jobspec = yaml.safe_load(source)
        if not isinstance(jobspec, dict):
            raise ValueError("jobspec must be a YAML mapping")
        output = json.dumps(jobspec, indent=2, allow_nan=False) + "\n"
        if args.output and args.output != "-":
            Path(args.output).write_text(output, encoding="utf-8")
        else:
            sys.stdout.write(output)
    except (OSError, ValueError, TypeError, yaml.YAMLError) as exc:
        parser.exit(1, f"Conversion failed: {exc}\n")


if __name__ == "__main__":
    main()
