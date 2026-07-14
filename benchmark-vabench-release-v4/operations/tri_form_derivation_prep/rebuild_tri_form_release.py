#!/usr/bin/env python3
"""Rebuild, audit, and seal the tracked tri-form release deterministically."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


PREP_ROOT = Path(__file__).resolve().parent
PACKAGE_ROOT = PREP_ROOT.parents[1]
RELEASE = PACKAGE_ROOT / "release" / "tri-form-v4-1200-draft"


def run(*args: object) -> None:
    command = [sys.executable, *(str(arg) for arg in args)]
    completed = subprocess.run(command, check=False, capture_output=True, text=True)
    if completed.returncode:
        raise SystemExit(
            f"command failed ({completed.returncode}): {' '.join(command)}\n"
            f"{completed.stdout}{completed.stderr}"
        )


def main() -> int:
    materializer = PREP_ROOT / "materialize_tri_form_release.py"
    exporter = PREP_ROOT / "export_tri_form_runtime.py"
    runtime_auditor = PREP_ROOT / "audit_runtime_export.py"
    evidence_recorder = PREP_ROOT / "record_runtime_ingestion_evidence.py"
    release_auditor = PREP_ROOT / "audit_tri_form_release.py"

    run(materializer, "--force")
    samples = (("v4-001", "G1"), ("v4-501", "G2"), ("v4-1001", "G5"))
    with tempfile.TemporaryDirectory(prefix="vabench-v4-rebuild-") as raw_tmp:
        tmp = Path(raw_tmp)
        runs: list[Path] = []
        for task, mode in samples:
            runtime = tmp / f"{task.lower()}-{mode.lower()}"
            run(
                exporter,
                "--task",
                task,
                "--mode",
                mode,
                "--working-token-budget",
                "32768",
                "--output",
                runtime,
            )
            run(
                runtime_auditor,
                "--run",
                runtime,
                "--output",
                runtime / "evidence" / "runtime_export_audit.json",
            )
            runs.append(runtime)

        evidence_args: list[object] = [evidence_recorder]
        for runtime in runs:
            evidence_args.extend(("--run", runtime))
        evidence_args.extend(("--output", RELEASE / "RUNTIME_INGESTION_EVIDENCE.json"))
        run(*evidence_args)

    run(
        release_auditor,
        "--output",
        RELEASE / "AUDIT_REPORT.json",
        "--seal-output",
        RELEASE / "RELEASE_SEAL.json",
    )
    print(json.dumps({"status": "pass", "release": str(RELEASE), "samples": samples}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
