#!/usr/bin/env python3

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
MARKDOWN_HARD_BREAK_EXTENSIONS = {".md"}


def list_repo_files() -> list[Path]:
    completed = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT_DIR,
        check=True,
        stdout=subprocess.PIPE,
    )

    repo_files = []
    for raw_path in completed.stdout.split(b"\0"):
        if not raw_path:
            continue

        relative_path = Path(raw_path.decode("utf-8", "surrogateescape"))
        absolute_path = ROOT_DIR / relative_path

        if absolute_path.is_file():
            repo_files.append(relative_path)

    return sorted(repo_files)


def is_binary_file(contents: bytes) -> bool:
    return b"\0" in contents


def find_line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def check_trailing_whitespace(relative_path: Path, text: str) -> list[str]:
    issues: list[str] = []
    allow_markdown_hard_breaks = relative_path.suffix.lower() in MARKDOWN_HARD_BREAK_EXTENSIONS

    for line_number, raw_line in enumerate(text.splitlines(keepends=True), start=1):
        if raw_line.endswith("\r\n"):
            line_content = raw_line[:-2]
        elif raw_line.endswith(("\n", "\r")):
            line_content = raw_line[:-1]
        else:
            line_content = raw_line

        stripped_line = line_content.rstrip(" \t")
        trailing_segment = line_content[len(stripped_line) :]

        if not trailing_segment:
            continue

        if allow_markdown_hard_breaks and trailing_segment == "  " and stripped_line:
            continue

        issues.append(f"{relative_path}:{line_number}: trailing whitespace")

    return issues


def check_file(relative_path: Path) -> list[str]:
    absolute_path = ROOT_DIR / relative_path
    contents = absolute_path.read_bytes()

    if is_binary_file(contents):
        return []

    text = contents.decode("utf-8", "surrogateescape")
    issues: list[str] = []

    carriage_return_index = text.find("\r")
    if carriage_return_index != -1:
        line_number = find_line_number(text, carriage_return_index)
        issues.append(f"{relative_path}:{line_number}: CRLF/CR line endings detected")

    if contents and not contents.endswith(b"\n"):
        issues.append(f"{relative_path}:EOF: missing final newline")

    issues.extend(check_trailing_whitespace(relative_path, text))

    return issues


def main() -> int:
    issues: list[str] = []

    for relative_path in list_repo_files():
        issues.extend(check_file(relative_path))

    if issues:
        print("Text hygiene issues found:", file=sys.stderr)
        for issue in issues:
            print(f"- {issue}", file=sys.stderr)
        print(
            "Run ./scripts/format-all.sh to apply the repository text fixers.",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
