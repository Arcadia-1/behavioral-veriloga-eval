#!/usr/bin/env python3
from __future__ import annotations

import fnmatch
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

ALLOWED_DIRS = {
    ".git",
    ".github",
    ".pytest_cache",
    "benchmark-vabench-release-v1",
    "conformance",
    "datasets",
    "docs",
    "examples",
    "experiments",
    "literature",
    "logs",
    "results",
    "runners",
    "schemas",
    "scripts",
    "speed-optimization",
    "tables",
    "tasks",
    "tests",
}

ALLOWED_FILES = {
    ".DS_Store",
    ".env.table2",
    ".git",
    ".gitignore",
    "AGENTS.md",
    "README.md",
    "pyproject.toml",
}

FORBIDDEN_NAMES = {
    "generated",
    "runlogs",
    "experiment-logs",
    "refine-logs",
    "scratch",
    "tmp",
}

FORBIDDEN_PATTERNS = (
    "generated-*",
    "results-*",
    "results_*",
)


def is_git_ignored(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    result = subprocess.run(
        ["git", "check-ignore", "-q", "--", rel],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def is_forbidden_root_name(name: str) -> bool:
    if name in FORBIDDEN_NAMES:
        return True
    return any(fnmatch.fnmatchcase(name, pattern) for pattern in FORBIDDEN_PATTERNS)


def main() -> int:
    violations: list[str] = []

    for entry in sorted(ROOT.iterdir(), key=lambda path: path.name):
        name = entry.name

        if is_forbidden_root_name(name):
            violations.append(
                f"forbidden top-level path: {name} "
                "(use results/<run-id>/ for active output, or archive raw output)"
            )
            continue

        if entry.is_dir():
            if name in ALLOWED_DIRS:
                continue
            if is_git_ignored(entry):
                continue
            violations.append(f"unexpected top-level directory: {name}")
            continue

        if entry.is_file() or entry.is_symlink():
            if name in ALLOWED_FILES:
                continue
            if is_git_ignored(entry):
                continue
            violations.append(f"unexpected top-level file: {name}")

    if violations:
        print("Repository layout violations:")
        for violation in violations:
            print(f"- {violation}")
        print("See docs/REPO_LAYOUT_POLICY.md")
        return 1

    print("Repository layout check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
