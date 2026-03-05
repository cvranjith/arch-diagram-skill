#!/usr/bin/env python3
"""Return the next versioned HTML output path.

Usage:
    python3 skill/scripts/next_version_path.py --project banking-agent --name data-flow

Output:
    output/banking-agent/data-flow-v1.html
"""

import argparse
import pathlib
import re


def to_kebab(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value)
    return value.strip("-")


def next_version(project: str, name: str, output_root: pathlib.Path) -> pathlib.Path:
    project_slug = to_kebab(project)
    name_slug = to_kebab(name)

    if not project_slug or not name_slug:
        raise ValueError("project and name must contain at least one alphanumeric character")

    project_dir = output_root / project_slug
    pattern = re.compile(rf"^{re.escape(name_slug)}-v(\d+)\.html$", re.IGNORECASE)

    highest = 0
    if project_dir.exists():
        for path in project_dir.glob("*.html"):
            match = pattern.match(path.name)
            if match:
                highest = max(highest, int(match.group(1)))

    return project_dir / f"{name_slug}-v{highest + 1}.html"


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute next diagram output version path")
    parser.add_argument("--project", required=True, help="Project slug or phrase")
    parser.add_argument("--name", required=True, help="Diagram file base name")
    parser.add_argument("--output-root", default="output", help="Output root directory")
    parser.add_argument("--mkdir", action="store_true", help="Create project directory")
    args = parser.parse_args()

    output_root = pathlib.Path(args.output_root)
    path = next_version(args.project, args.name, output_root)

    if args.mkdir:
        path.parent.mkdir(parents=True, exist_ok=True)

    print(path.as_posix())


if __name__ == "__main__":
    main()
