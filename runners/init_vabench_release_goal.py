#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TAXONOMY_PATH = ROOT / "docs" / "VABENCH_RELEASE_TAXONOMY.md"
GOAL_PATH = ROOT / "docs" / "VABENCH_LONGRUN_GOAL.md"
TRACKER_CSV = ROOT / "docs" / "VABENCH_RELEASE_TRACKER.csv"
TRACKER_MD = ROOT / "docs" / "VABENCH_RELEASE_TRACKER.md"
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
RELEASE_TASK_SCHEMA = ROOT / "schemas" / "vabench-release-task.schema.json"
RELEASE_ENTRY_SCHEMA = ROOT / "schemas" / "vabench-release-entry.schema.json"
PACKAGE_MANIFEST_SCHEMA = ROOT / "schemas" / "vabench-package-manifest.schema.json"
EVALUATOR_CONTRACT_SCHEMA = ROOT / "schemas" / "vabench-evaluator-contract.schema.json"
SPEED_DEBUG_ARTIFACT_SCHEMA = ROOT / "schemas" / "vabench-speed-debug-artifact.schema.json"
BASELINE_ARTIFACT_SCHEMA = ROOT / "schemas" / "vabench-baseline-artifact.schema.json"
PAPER_ARTIFACTS_SCHEMA = ROOT / "schemas" / "vabench-paper-artifacts.schema.json"
CLAIM_GATE_SCHEMA = ROOT / "schemas" / "vabench-claim-gate.schema.json"
SCORE_DENOMINATOR_SCHEMA = ROOT / "schemas" / "vabench-score-denominator.schema.json"
DUAL_RERUN_QUEUE_SCHEMA = ROOT / "schemas" / "vabench-dual-rerun-queue.schema.json"
DUAL_RERUN_STAGING_SCHEMA = ROOT / "schemas" / "vabench-dual-rerun-staging.schema.json"
DUAL_RERUN_IMPORT_SCHEMA = ROOT / "schemas" / "vabench-dual-rerun-import.schema.json"
BRIDGE_DIAGNOSTICS_SCHEMA = ROOT / "schemas" / "vabench-bridge-diagnostics.schema.json"
EXTERNAL_BLOCKERS_SCHEMA = ROOT / "schemas" / "vabench-external-blockers.schema.json"
FINISH_READINESS_SCHEMA = ROOT / "schemas" / "vabench-finish-readiness.schema.json"
COMPLETION_AUDIT_SCHEMA = ROOT / "schemas" / "vabench-completion-audit.schema.json"
FINISH_AFTER_BRIDGE_ATTEMPT_SCHEMA = ROOT / "schemas" / "vabench-finish-after-bridge-attempt.schema.json"
CONFORMANCE_MANIFEST_SCHEMA = ROOT / "schemas" / "vabench-conformance-manifest.schema.json"
ARTIFACT_INDEX_SCHEMA = ROOT / "schemas" / "vabench-artifact-index.schema.json"
CHECKSUM_MANIFEST_SCHEMA = ROOT / "schemas" / "vabench-checksum-manifest.schema.json"
PAPER_TABLES_SCHEMA = ROOT / "schemas" / "vabench-paper-tables.schema.json"
RELEASE_TASK_MANIFEST_SYNC_SCHEMA = ROOT / "schemas" / "vabench-release-task-manifest-sync.schema.json"
RELEASE_STATUS_SCHEMA = ROOT / "schemas" / "vabench-release-status.schema.json"
ASSET_INTEGRITY_SCHEMA = ROOT / "schemas" / "vabench-asset-integrity.schema.json"
STATIC_CERTIFICATION_SCHEMA = ROOT / "schemas" / "vabench-static-certification.schema.json"
DUAL_CERTIFICATION_SCHEMA = ROOT / "schemas" / "vabench-dual-certification.schema.json"
CERTIFICATION_MATRIX_SCHEMA = ROOT / "schemas" / "vabench-certification-matrix.schema.json"
REMAINING_WORK_SCHEMA = ROOT / "schemas" / "vabench-remaining-work.schema.json"
EVIDENCE_SCHEMA = ROOT / "schemas" / "vabench-evidence.schema.json"
RESULT_SCHEMA = ROOT / "schemas" / "vabench-release-result.schema.json"


TRACKER_FIELDS = [
    "entry_id",
    "category",
    "base_function",
    "level",
    "package_status",
    "release_status",
    "score_surface",
    "required_task_forms",
    "complete_circuit_form",
    "materialization_status",
    "prompt_status",
    "meta_status",
    "checks_status",
    "gold_status",
    "static_status",
    "evas_status",
    "spectre_status",
    "certification_status",
    "evidence_link",
    "notes",
]


def slugify(value: str) -> str:
    value = value.lower().replace("/", " ")
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def parse_release_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    in_table = False
    for raw in TAXONOMY_PATH.read_text(encoding="utf-8").splitlines():
        if raw.startswith("## Release Coverage Table"):
            in_table = True
            continue
        if in_table and raw.startswith("## "):
            break
        if not in_table or not raw.startswith("|"):
            continue
        parts = [part.strip() for part in raw.strip().strip("|").split("|")]
        if len(parts) != 8 or parts[0] in {"Category", "---"}:
            continue
        category, base, level, form, task_forms, surface, status, cert = parts
        if level not in {"L1", "L2"}:
            continue
        rows.append(
            {
                "category": category,
                "base_function": base,
                "level": level,
                "complete_circuit_form": form,
                "required_task_forms": task_forms,
                "score_surface": surface,
                "release_status": status,
                "certification_status_from_taxonomy": cert,
            }
        )
    return rows


def package_status(row: dict[str, str]) -> str:
    status = row["release_status"]
    level = row["level"]
    if level == "L2":
        return "selected_l2_target"
    if status == "Required expansion":
        return "selected_l1_addition"
    if status == "Required with review":
        return "current_l1_seed_with_review"
    return "current_l1_seed"


def tracker_row(row: dict[str, str]) -> dict[str, str]:
    level = row["level"].lower()
    base_slug = slugify(row["base_function"])
    status = package_status(row)
    return {
        "entry_id": f"vbr1_{level}_{base_slug}",
        "category": row["category"],
        "base_function": row["base_function"],
        "level": row["level"],
        "package_status": status,
        "release_status": row["release_status"],
        "score_surface": row["score_surface"],
        "required_task_forms": row["required_task_forms"],
        "complete_circuit_form": row["complete_circuit_form"],
        "materialization_status": "source_review_pending" if status.startswith("current") else "missing",
        "prompt_status": "pending",
        "meta_status": "pending",
        "checks_status": "pending",
        "gold_status": "pending",
        "static_status": "pending",
        "evas_status": "pending",
        "spectre_status": "pending",
        "certification_status": "not_certified",
        "evidence_link": "",
        "notes": "Generated from VABENCH_RELEASE_TAXONOMY; do not score until certified.",
    }


def write_tracker(rows: list[dict[str, str]]) -> None:
    tracker = [tracker_row(row) for row in rows]
    with TRACKER_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=TRACKER_FIELDS)
        writer.writeheader()
        writer.writerows(tracker)

    counts: dict[str, int] = {}
    for row in tracker:
        counts[row["package_status"]] = counts.get(row["package_status"], 0) + 1

    lines = [
        "# vaBench Release Tracker",
        "",
        f"Date: {date.today().isoformat()}",
        "",
        "This tracker is generated from `docs/VABENCH_RELEASE_TAXONOMY.md`.",
        "It is the execution queue for the long-run vaBench release goal.",
        "",
        "## Count Summary",
        "",
        "| Status | Count |",
        "| --- | ---: |",
    ]
    for key in sorted(counts):
        lines.append(f"| {key} | {counts[key]} |")
    lines.extend(
        [
            f"| total | {len(tracker)} |",
            "",
            "## Certification Rule",
            "",
            "A row enters the scored benchmark only after `certification_status=certified`",
            "and after prompt, metadata, checks, gold assets, static checks, EVAS,",
            "and Spectre are all marked complete/pass.",
            "",
            "## Tracker Rows",
            "",
            "| Entry | Level | Category | Function | Package status | Certification |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in tracker:
        lines.append(
            "| {entry_id} | {level} | {category} | {base_function} | {package_status} | {certification_status} |".format(
                **row
            )
        )
    TRACKER_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_goal() -> None:
    GOAL_PATH.write_text(
        """# vaBench Long-Run Goal

Date: {today}

## Objective

Build the clean vaBench release package from the 75-entry top-level L1/L2
coverage target. The release must contain public prompts, metadata, checks,
gold assets, EVAS/Spectre certification evidence, and paper-facing reports.

## Non-Negotiable Invariants

- Do not score uncertified rows.
- Keep L0 EVAS/Spectre conformance outside the L1/L2 benchmark denominator.
- Keep current-domain, KCL/KVL, transistor-level, AC/noise, and device physics
  outside this release unless the project scope is explicitly changed.
- Do not revive controller/RAG/SFT/workflow engineering as the core
  contribution.
- Spectre remains the final certification reference; EVAS remains the fast
  debug evaluator.

## Execution Surface

- Tracker: `docs/VABENCH_RELEASE_TRACKER.csv`
- Human tracker: `docs/VABENCH_RELEASE_TRACKER.md`
- Release package root: `benchmark-vabench-release-v1/`
- Release entry schema: `schemas/vabench-release-entry.schema.json`
- Release task schema: `schemas/vabench-release-task.schema.json`
- Evidence schema: `schemas/vabench-evidence.schema.json`
- Result schema: `schemas/vabench-release-result.schema.json`

## Required End State

1. Every tracker row has a release task or an explicit documented exclusion.
2. Every scored row has reviewed `prompt.md`, `meta.json`, `checks.yaml`,
   `gold/`, `evidence.json`, and `result.json`.
3. EVAS/Spectre dual certification has zero EVAS PASS / Spectre FAIL rows.
4. L0 conformance cases explain known syntax, source, event, sampling, and
   checker semantic risks.
5. Paper-facing reports include coverage, certification, parity, speed/debug,
   and baseline summaries.
6. A completion audit maps each goal requirement to current evidence and keeps
   blocked or pending items out of the completed state.
7. An artifact index maps schemas, trackers, reports, and rerun commands to
   their paper-facing claim roles.
8. Schema validation covers release entries, release task manifests, evidence,
   and result JSON surfaces.
9. A checksum manifest hashes release package, release docs, and schema files
   for reproducible paper-facing artifacts.
10. A score denominator manifest is the source of truth for scored entries and
   forms, and it keeps all uncertified rows out of reported model scores.

## Single Long-Run Policy

Do not expand this release by hand-sized batches. The runner should traverse
the full 75-entry tracker every time. Entries with release-ready source assets
are materialized immediately; entries without release-ready source assets are
kept as explicit pending package skeletons. Missing EVAS/Spectre evidence is a
pending certification blocker, not a simulator failure and not a scored result.

## Current Checkpoint

The current automated release run materializes 75 planned L1/L2 entries and
259 release forms. Static/integrity certification is regenerated from the clean
package assets. Historical dual evidence certifies the current imported subset,
while remaining primary forms are staged and ready
for a fresh EVAS/Spectre rerun. The remaining simulator blocker is external
bridge access: stale or partial rerun summaries are explicitly rejected by the
import gate until a fresh complete rerun exists.

The current verification command is:

```bash
python3 runners/run_vabench_release_longrun.py
```

It regenerates release package artifacts and runs the release test suite. Treat
the pytest summary printed by this command as the current local verification
evidence.

## Long-Run Command Pattern

Use this objective for the long process:

```text
Materialize and certify the clean vaBench release from docs/VABENCH_RELEASE_TRACKER.csv.
For each row, create or update the release task under benchmark-vabench-release-v1/tasks,
write prompt/meta/checks/gold assets, run static checks, stage EVAS and Spectre
certification bundles, import only complete rerun evidence, update evidence/result
files, and update the tracker. Do not score or claim any row until certification
passes. Keep L0 conformance separate.
```

## Automation Commands

Bootstrap, materialize, statically certify, prepare rerun staging, and refresh
claim-gated reports:

```bash
python3 runners/run_vabench_release_longrun.py
```

Run the primary EVAS/Spectre release rerun when the Virtuoso bridge is ready:

```bash
./scripts/run_with_bridge.sh python3 runners/run_vabench_release_dual_rerun.py \\
  --output-root results/vabench-release-v1-dual-rerun \\
  --timeout-s 180
```

Or use the one-command finish path, which tries bridge profiles, imports only
complete rerun evidence, and refreshes speed/baseline/paper/completion reports:

```bash
python3 runners/finish_vabench_release_after_bridge.py
```

The rerun consumes
`benchmark-vabench-release-v1/reports/dual_rerun_staging_manifest.json`.
By default it runs only primary pass bundles (`gold` and bugfix `fixed`). Use
`--include-buggy` only for the separate badcase confirmation lane.

The bridge wrapper is fail-fast and claim-gated:

- `VB_SSH_CONNECT_TIMEOUT`, `VB_SSH_SERVER_ALIVE_INTERVAL`, and
  `VB_SSH_SERVER_ALIVE_COUNT_MAX` bound SSH tunnel startup.
- Set `BRIDGE_PROFILE=jin` or another profile name to route through
  `VB_*_<profile>` values from the bridge `.env` without editing the file.
- Set `VB_USE_SSH_CONFIG_JUMP=1` when the bridge `.env` `VB_JUMP_HOST`
  conflicts with the local SSH `ProxyJump`; this lets `ssh` use the local
  `~/.ssh/config` route instead of passing an explicit `-J`.
- If tunnel startup fails before the release rerun runner starts, the wrapper
  asks `run_vabench_release_dual_rerun.py` to write only a blocked summary;
  it does not enable simulator direct-run fallback.
- A blocked summary is never imported as certification evidence.
- `benchmark-vabench-release-v1/reports/completion_audit.json` is the final
  per-run completion gate. It must remain `in_progress` until every required
  item is proved by current artifacts.
- `benchmark-vabench-release-v1/reports/artifact_index.json` is the
  traceability index for paper-facing artifacts and reproducible commands.
- `benchmark-vabench-release-v1/reports/schema_validation.json` validates
  release entries, per-form release task manifests, evaluator contract,
  score denominator, speed/debug, baseline, paper artifacts, claim gates,
  dual rerun gates, bridge/readiness gates, evidence, and results.
- `benchmark-vabench-release-v1/reports/score_denominator_manifest.json` is
  the only source of truth for scored entry/form denominators.
- `benchmark-vabench-release-v1/reports/checksum_manifest.json` records
  SHA-256 hashes for release artifacts, excluding itself.
""".format(today=date.today().isoformat()),
        encoding="utf-8",
    )


def write_package_readme() -> None:
    PACKAGE_ROOT.mkdir(exist_ok=True)
    for child in ("tasks", "conformance", "evidence", "reports"):
        path = PACKAGE_ROOT / child
        path.mkdir(parents=True, exist_ok=True)
        (path / ".gitkeep").write_text("", encoding="utf-8")
    (PACKAGE_ROOT / "README.md").write_text(
        """# vaBench Release Package v1

This directory is the clean paper-facing benchmark package for the 75-entry L1/L2
vaBench release target. It is intentionally claim-gated: source assets,
static checks, imported EVAS/Spectre evidence, fresh rerun staging, score
denominators, speed/debug measurements, and model baselines are reported as
separate surfaces.

The package can be cited only through the current reports in `reports/`. A row
is not part of the scored benchmark until its score-denominator report marks it
as counted, and no pending or blocked simulator run is certification evidence.

## Layout

- `tasks/`: scored L1/L2 task directories after materialization.
- `conformance/`: non-scored L0 EVAS/Spectre diagnostic cases.
- `evidence/`: certification bundles and simulator logs referenced by tasks.
- `reports/`: coverage, parity, speed/debug, baseline, completion, artifact
  index, claim gate, and paper table summaries.
- `rerun_staging/`: staged runnable bundles for the fresh EVAS/Spectre rerun.

Rows are planned in `../docs/VABENCH_RELEASE_TRACKER.csv`. A row is not part of
the scored benchmark until its task assets and EVAS/Spectre evidence are
complete.

Current seed rows may contain `forms/<form>/` directories copied from reviewed
source tasks. These copied assets are release-materialized, but still unscored
until static, EVAS, and Spectre certification are attached.

L0 conformance assets are synchronized from `../conformance/evas-spectre/`.
They are simulator diagnostics and do not count toward L1/L2 benchmark coverage,
model capability, bugfix claims, or broad parity denominators.

## Current Claim Boundary

The current local package is source-complete and statically certified, but not
fully release-certified until the fresh EVAS/Spectre rerun completes and imports
successfully.

Use these reports as the source of truth:

- `reports/claim_gate.json`: allowed and blocked paper claims with safe wording.
- `reports/paper_tables.json`: CSV/Markdown table exports for paper drafting.
- `reports/completion_audit.json`: requirement-by-requirement completion gate.
- `reports/artifact_index.json`: traceability index for artifacts and commands.
- `reports/score_denominator_manifest.json`: only source of truth for scored
  entries/forms.
- `reports/external_blockers.json`: external bridge/rerun/import blocker chain.
- `reports/finish_readiness.json`: preflight gate for safely starting,
  importing, and finishing the fresh EVAS/Spectre release rerun.
- `MANIFEST.json`: package-level machine-readable index for entries, forms,
  assets, evidence links, certification status, and score inclusion.
- `EVALUATOR.json`: machine-readable evaluator contract for task selection,
  backend roles, result/evidence schemas, score gates, and baseline lanes.

Current safe wording is intentionally narrow:

- The package defines a 75-entry L1/L2 coverage target.
- All materialized release forms pass static/integrity checks.
- The imported certified EVAS/Spectre subset is clean with respect to
  EVAS PASS / Spectre FAIL mismatches.
- L0 conformance is separate from the benchmark denominator.

Do not claim full release certification, scored benchmark results, EVAS speedup,
debug advantage, or model baselines until the corresponding claim gate is
allowed.

## Reproducible Commands

Regenerate the local release package, reports, schema validation, checksums, and
tests:

```bash
python3 runners/run_vabench_release_longrun.py
```

After the external Virtuoso bridge is reachable, finish the fresh dual rerun,
import only complete results, and refresh downstream reports:

```bash
python3 runners/finish_vabench_release_after_bridge.py
```

The direct rerun command is:

```bash
./scripts/run_with_bridge.sh python3 runners/run_vabench_release_dual_rerun.py \\
  --output-root results/vabench-release-v1-dual-rerun \\
  --timeout-s 180
```

Blocked or dry-run summaries must not be imported as certification evidence.
Use `reports/bridge_profile_diagnostics.json` and
`reports/external_blockers.json` to decide whether the bridge is ready. Use
`reports/finish_readiness.json` before importing any fresh rerun summary.
""",
        encoding="utf-8",
    )


def write_schemas() -> None:
    release_entry_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "vaBench release entry skeleton",
        "type": "object",
        "required": [
            "id",
            "benchmark",
            "release_entry_id",
            "level",
            "category",
            "base_function",
            "package_status",
            "score_surface",
            "source_base_id",
            "source_tasks",
            "release_tasks",
            "missing_forms",
            "certification",
            "counts",
            "release_blockers",
        ],
        "properties": {
            "id": {"type": "string"},
            "benchmark": {"const": "vabench-release-v1"},
            "release_entry_id": {"type": "string"},
            "level": {"enum": ["L1", "L2"]},
            "category": {"type": "string"},
            "base_function": {"type": "string"},
            "package_status": {
                "enum": [
                    "current_l1_seed",
                    "current_l1_seed_with_review",
                    "selected_l1_addition",
                    "selected_l2_target",
                ]
            },
            "score_surface": {"enum": ["model-capability", "benchmark-e2e"]},
            "source_base_id": {"type": "string"},
            "canonical_kernel": {"type": "string"},
            "source_registry_status": {"type": "string"},
            "source_evidence_status": {"type": "string"},
            "source_tasks": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["form", "source_path", "prompt", "meta", "checks", "gold", "asset_complete"],
                    "properties": {
                        "form": {"enum": ["dut", "tb", "bugfix", "e2e"]},
                        "source_path": {"type": "string"},
                        "prompt": {"type": "boolean"},
                        "meta": {"type": "boolean"},
                        "checks": {"type": "boolean"},
                        "gold": {"type": "boolean"},
                        "asset_complete": {"type": "boolean"},
                    },
                },
            },
            "release_tasks": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": [
                        "form",
                        "release_path",
                        "prompt",
                        "meta",
                        "checks",
                        "gold",
                        "asset_materialized",
                    ],
                    "properties": {
                        "form": {"enum": ["dut", "tb", "bugfix", "e2e"]},
                        "release_path": {"type": "string"},
                        "prompt": {"type": "string"},
                        "meta": {"type": "string"},
                        "checks": {"type": "string"},
                        "gold": {"type": "array", "items": {"type": "string"}},
                        "asset_materialized": {"type": "boolean"},
                    },
                },
            },
            "missing_forms": {
                "type": "array",
                "items": {"enum": ["dut", "tb", "bugfix", "e2e"]},
            },
            "certification": {
                "type": "object",
                "required": ["static", "evas", "spectre", "evidence"],
                "properties": {
                    "static": {"enum": ["pending", "pass", "fail"]},
                    "evas": {"enum": ["pending", "pass", "fail"]},
                    "spectre": {"enum": ["pending", "pass", "fail"]},
                    "evidence": {"type": "string"},
                },
            },
            "counts": {
                "type": "object",
                "required": ["benchmark_score", "model_capability", "l0_conformance"],
                "properties": {
                    "benchmark_score": {"const": False},
                    "model_capability": {"const": False},
                    "l0_conformance": {"const": False},
                },
            },
            "release_blockers": {"type": "array", "items": {"type": "string"}},
        },
        "additionalProperties": True,
    }
    release_task_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "vaBench release task",
        "type": "object",
        "required": [
            "id",
            "benchmark",
            "release_entry_id",
            "level",
            "category",
            "base_function",
            "family",
            "domain",
            "score_surface",
            "artifacts",
            "certification",
            "counts",
        ],
        "properties": {
            "id": {"type": "string"},
            "benchmark": {"const": "vabench-release-v1"},
            "release_entry_id": {"type": "string"},
            "level": {"enum": ["L1", "L2"]},
            "category": {"type": "string"},
            "base_function": {"type": "string"},
            "family": {"enum": ["spec-to-va", "tb-generation", "bugfix", "end-to-end"]},
            "domain": {"const": "voltage"},
            "score_surface": {"enum": ["model-capability", "benchmark-e2e"]},
            "artifacts": {
                "type": "object",
                "required": ["prompt", "meta", "checks", "gold"],
                "properties": {
                    "prompt": {"type": "string"},
                    "meta": {"type": "string"},
                    "checks": {"type": "string"},
                    "gold": {"type": "array", "items": {"type": "string"}},
                },
            },
            "certification": {
                "type": "object",
                "required": ["static", "evas", "spectre", "evidence"],
                "properties": {
                    "static": {"enum": ["pending", "pass", "fail"]},
                    "evas": {"enum": ["pending", "pass", "fail"]},
                    "spectre": {"enum": ["pending", "pass", "fail"]},
                    "evidence": {"type": "string"},
                },
            },
            "counts": {
                "type": "object",
                "required": ["benchmark_score", "model_capability", "l0_conformance"],
                "properties": {
                    "benchmark_score": {"type": "boolean"},
                    "model_capability": {"type": "boolean"},
                    "l0_conformance": {"const": False},
                },
            },
        },
        "additionalProperties": True,
    }
    evidence_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "vaBench certification evidence",
        "type": "object",
        "required": ["release_entry_id", "task_id", "taxonomy", "static", "evas", "spectre", "verdict"],
        "properties": {
            "release_entry_id": {"type": "string"},
            "task_id": {"type": "string"},
            "taxonomy": {
                "type": "object",
                "required": ["level", "category", "base_function"],
                "properties": {
                    "level": {"enum": ["L1", "L2", "L0"]},
                    "category": {"type": "string"},
                    "base_function": {"type": "string"},
                },
            },
            "static": {"enum": ["pending", "pass", "fail"]},
            "evas": {"enum": ["pending", "pass", "fail"]},
            "spectre": {"enum": ["pending", "pass", "fail"]},
            "verdict": {"enum": ["not_certified", "certified", "quarantined"]},
            "artifacts": {"type": "array", "items": {"type": "string"}},
            "notes": {"type": "string"},
        },
        "additionalProperties": True,
    }
    result_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "vaBench release result",
        "type": "object",
        "required": ["task_id", "backend", "status", "scores", "artifacts"],
        "properties": {
            "task_id": {"type": "string"},
            "release_entry_id": {"type": "string"},
            "backend": {"enum": ["static", "evas", "spectre"]},
            "status": {
                "enum": [
                    "PASS",
                    "FAIL_STATIC",
                    "FAIL_DUT_COMPILE",
                    "FAIL_TB_COMPILE",
                    "FAIL_SIM_CORRECTNESS",
                    "FAIL_INFRA",
                    "PENDING",
                ]
            },
            "scores": {"type": "object"},
            "artifacts": {"type": "array", "items": {"type": "string"}},
            "notes": {"type": "array", "items": {"type": "string"}},
        },
        "additionalProperties": True,
    }
    package_manifest_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "vaBench release package manifest",
        "type": "object",
        "required": [
            "date",
            "release",
            "status",
            "package_root",
            "summary",
            "entries",
            "forms",
            "reports",
            "claim_boundary",
        ],
        "properties": {
            "date": {"type": "string"},
            "release": {"const": "vabench-release-v1"},
            "status": {"enum": ["in_progress", "complete"]},
            "package_root": {"const": "benchmark-vabench-release-v1"},
            "summary": {
                "type": "object",
                "required": [
                    "planned_entry_count",
                    "entry_count",
                    "form_count",
                    "certified_entry_count",
                    "certified_form_count",
                    "scored_entry_count",
                    "scored_form_count",
                    "l0_conformance_case_count",
                ],
                "properties": {
                    "planned_entry_count": {"type": "integer"},
                    "entry_count": {"type": "integer"},
                    "form_count": {"type": "integer"},
                    "certified_entry_count": {"type": "integer"},
                    "certified_form_count": {"type": "integer"},
                    "scored_entry_count": {"type": "integer"},
                    "scored_form_count": {"type": "integer"},
                    "l0_conformance_case_count": {"type": "integer"},
                },
            },
            "entries": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": [
                        "release_entry_id",
                        "level",
                        "category",
                        "base_function",
                        "release_entry_manifest",
                        "form_count",
                        "forms",
                        "certification",
                        "counted_in_score",
                    ],
                    "properties": {
                        "release_entry_id": {"type": "string"},
                        "level": {"enum": ["L1", "L2"]},
                        "category": {"type": "string"},
                        "base_function": {"type": "string"},
                        "release_entry_manifest": {"type": "string"},
                        "form_count": {"type": "integer"},
                        "forms": {"type": "array", "items": {"enum": ["dut", "tb", "bugfix", "e2e"]}},
                        "certification": {"type": "string"},
                        "counted_in_score": {"type": "boolean"},
                    },
                    "additionalProperties": True,
                },
            },
            "forms": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": [
                        "task_id",
                        "release_entry_id",
                        "form",
                        "family",
                        "release_task_manifest",
                        "static",
                        "evas",
                        "spectre",
                        "counted_in_score",
                    ],
                    "properties": {
                        "task_id": {"type": "string"},
                        "release_entry_id": {"type": "string"},
                        "form": {"enum": ["dut", "tb", "bugfix", "e2e"]},
                        "family": {"enum": ["spec-to-va", "tb-generation", "bugfix", "end-to-end"]},
                        "release_task_manifest": {"type": "string"},
                        "static": {"enum": ["pending", "pass", "fail"]},
                        "evas": {"enum": ["pending", "pass", "fail"]},
                        "spectre": {"enum": ["pending", "pass", "fail"]},
                        "counted_in_score": {"type": "boolean"},
                    },
                    "additionalProperties": True,
                },
            },
            "reports": {"type": "object"},
            "claim_boundary": {"type": "array", "items": {"type": "string"}},
        },
        "additionalProperties": True,
    }
    evaluator_contract_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "vaBench release evaluator contract",
        "type": "object",
        "required": [
            "date",
            "release",
            "status",
            "contract_version",
            "inputs",
            "schemas",
            "task_selection",
            "backend_roles",
            "result_contract",
            "score_gate",
            "baseline_protocol",
            "commands",
            "claim_boundary",
        ],
        "properties": {
            "date": {"type": "string"},
            "release": {"const": "vabench-release-v1"},
            "status": {"enum": ["ready", "in_progress", "blocked"]},
            "contract_version": {"type": "string"},
            "inputs": {"type": "object"},
            "schemas": {
                "type": "object",
                "required": [
                    "release_entry",
                    "release_task",
                    "evidence",
                    "result",
                    "package_manifest",
                    "evaluator_contract",
                    "speed_debug_artifact",
                    "baseline_artifact",
                    "paper_artifacts",
                    "claim_gate",
                    "score_denominator",
                    "dual_rerun_queue",
                    "dual_rerun_staging",
                    "dual_rerun_import",
                    "bridge_diagnostics",
                    "external_blockers",
                    "finish_readiness",
                    "completion_audit",
                    "finish_after_bridge_attempt",
                    "conformance_manifest",
                    "artifact_index",
                    "checksum_manifest",
                    "paper_tables",
                    "release_task_manifest_sync",
                    "release_status",
                    "asset_integrity",
                    "static_certification",
                    "dual_certification",
                    "certification_matrix",
                    "remaining_work",
                ],
                "properties": {
                    "release_entry": {"type": "string"},
                    "release_task": {"type": "string"},
                    "evidence": {"type": "string"},
                    "result": {"type": "string"},
                    "package_manifest": {"type": "string"},
                    "evaluator_contract": {"type": "string"},
                    "speed_debug_artifact": {"type": "string"},
                    "baseline_artifact": {"type": "string"},
                    "paper_artifacts": {"type": "string"},
                    "claim_gate": {"type": "string"},
                    "score_denominator": {"type": "string"},
                    "dual_rerun_queue": {"type": "string"},
                    "dual_rerun_staging": {"type": "string"},
                    "dual_rerun_import": {"type": "string"},
                    "bridge_diagnostics": {"type": "string"},
                    "external_blockers": {"type": "string"},
                    "finish_readiness": {"type": "string"},
                    "completion_audit": {"type": "string"},
                    "finish_after_bridge_attempt": {"type": "string"},
                    "conformance_manifest": {"type": "string"},
                    "artifact_index": {"type": "string"},
                    "checksum_manifest": {"type": "string"},
                    "paper_tables": {"type": "string"},
                    "release_task_manifest_sync": {"type": "string"},
                    "release_status": {"type": "string"},
                    "asset_integrity": {"type": "string"},
                    "static_certification": {"type": "string"},
                    "dual_certification": {"type": "string"},
                    "certification_matrix": {"type": "string"},
                    "remaining_work": {"type": "string"},
                },
            },
            "task_selection": {
                "type": "object",
                "required": [
                    "source_of_truth",
                    "scored_entries",
                    "scored_forms",
                    "l0_conformance_excluded",
                    "unscored_rows_excluded",
                ],
                "properties": {
                    "source_of_truth": {"type": "string"},
                    "scored_entries": {"type": "integer"},
                    "scored_forms": {"type": "integer"},
                    "l0_conformance_excluded": {"type": "boolean"},
                    "unscored_rows_excluded": {"type": "boolean"},
                },
            },
            "backend_roles": {"type": "object"},
            "result_contract": {"type": "object"},
            "score_gate": {"type": "object"},
            "baseline_protocol": {"type": "object"},
            "commands": {"type": "object"},
            "claim_boundary": {"type": "array", "items": {"type": "string"}},
        },
        "additionalProperties": True,
    }
    speed_debug_artifact_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "vaBench speed/debug artifact",
        "type": "object",
        "required": [
            "date",
            "release",
            "status",
            "claim_allowed",
            "measurement_scope",
            "measurement_plan",
            "timing_totals",
            "required_to_claim",
            "debug_triage_order",
            "rows",
        ],
        "properties": {
            "date": {"type": "string"},
            "release": {"const": "vabench-release-v1"},
            "status": {
                "enum": [
                    "pending_measurement",
                    "measured_subset",
                    "measured",
                    "measured_with_failures",
                ]
            },
            "claim_allowed": {"type": "boolean"},
            "reason": {"type": "string"},
            "measurement_scope": {
                "type": "object",
                "required": [
                    "planned_primary_rerun_rows",
                    "planned_staged_bundles",
                    "timed_rows",
                ],
                "properties": {
                    "planned_primary_rerun_rows": {"type": "integer"},
                    "planned_staged_bundles": {"type": "integer"},
                    "timed_rows": {"type": "integer"},
                    "scored_form_count": {"type": "integer"},
                    "timed_scored_form_count": {"type": "integer"},
                    "full_score_denominator_timed": {"type": "boolean"},
                },
            },
            "measurement_plan": {
                "type": "object",
                "required": [
                    "status",
                    "bridge_ready",
                    "primary_queue_rows",
                    "staged_bundle_count",
                    "required_timing_fields",
                    "claim_blockers",
                ],
                "properties": {
                    "status": {
                        "enum": [
                            "measured_or_ready_to_import",
                            "ready_to_measure",
                            "blocked_by_bridge",
                            "blocked_by_staging",
                        ]
                    },
                    "bridge_ready": {"type": "boolean"},
                    "primary_queue_rows": {"type": "integer"},
                    "staged_bundle_count": {"type": "integer"},
                    "required_timing_fields": {"type": "array", "items": {"type": "string"}},
                    "claim_blockers": {"type": "array", "items": {"type": "string"}},
                },
            },
            "timing_totals": {
                "type": "object",
                "required": [
                    "evas_wall_time_s",
                    "spectre_wall_time_s",
                    "spectre_over_evas_speedup",
                ],
            },
            "timing_distribution": {"type": "object"},
            "required_to_claim": {"type": "array", "items": {"type": "string"}},
            "debug_triage_order": {"type": "array", "items": {"type": "string"}},
            "rows": {"type": "array", "items": {"type": "object"}},
        },
        "additionalProperties": True,
    }
    baseline_artifact_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "vaBench baseline artifact",
        "type": "object",
        "required": [
            "date",
            "release",
            "status",
            "claim_allowed",
            "scored_release_entries",
            "scored_release_forms",
            "score_denominator_status",
            "score_denominator",
            "fully_certified_entry_count",
            "dual_pending_release_task_count",
            "dual_failed_release_task_count",
            "baseline_summary_count",
            "baseline_summaries",
            "execution_plan",
            "baseline_protocol",
            "required_to_claim",
        ],
        "properties": {
            "date": {"type": "string"},
            "release": {"const": "vabench-release-v1"},
            "status": {"enum": ["pending_release_baselines", "ready_for_baseline_runs"]},
            "claim_allowed": {"type": "boolean"},
            "scored_release_entries": {"type": "integer"},
            "scored_release_forms": {"type": "integer"},
            "score_denominator_status": {"type": "string"},
            "score_denominator": {"type": "string"},
            "fully_certified_entry_count": {"type": "integer"},
            "dual_pending_release_task_count": {"type": "integer"},
            "dual_failed_release_task_count": {"type": "integer"},
            "baseline_summary_count": {"type": "integer"},
            "baseline_summaries": {"type": "array", "items": {"type": "string"}},
            "execution_plan": {
                "type": "object",
                "required": ["status", "blocked_by", "run_order", "aggregation_metrics"],
                "properties": {
                    "status": {"enum": ["ready_for_baseline_runs", "blocked_until_scored_release_exists"]},
                    "blocked_by": {"type": "array", "items": {"type": "string"}},
                    "run_order": {"type": "array", "items": {"type": "string"}},
                    "aggregation_metrics": {"type": "array", "items": {"type": "string"}},
                },
            },
            "baseline_protocol": {
                "type": "object",
                "required": ["minimal_lanes", "non_goals", "required_result_fields", "result_schema_contract"],
                "properties": {
                    "minimal_lanes": {"type": "array", "items": {"type": "string"}},
                    "non_goals": {"type": "array", "items": {"type": "string"}},
                    "required_result_fields": {"type": "array", "items": {"type": "string"}},
                    "result_schema_contract": {"type": "object"},
                },
            },
            "required_to_claim": {"type": "array", "items": {"type": "string"}},
        },
        "additionalProperties": True,
    }
    paper_artifacts_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "vaBench paper-facing artifact summary",
        "type": "object",
        "required": [
            "date",
            "release",
            "status",
            "coverage_summary",
            "parity_summary",
            "speed_debug_summary",
            "baseline_summary",
            "certification_gap_summary",
            "claim_gates",
            "evidence_sources",
            "remaining_counts",
        ],
        "properties": {
            "date": {"type": "string"},
            "release": {"const": "vabench-release-v1"},
            "status": {"enum": ["in_progress", "complete"]},
            "coverage_summary": {
                "type": "object",
                "required": [
                    "planned_entries",
                    "level_counts",
                    "source_linked_entry_count",
                    "asset_materialized_entry_count",
                    "static_certified_release_task_count",
                    "dual_certified_release_task_count",
                    "scored_release_entries",
                    "scored_release_forms",
                    "score_denominator_status",
                    "claim_status",
                ],
                "properties": {
                    "planned_entries": {"type": "integer"},
                    "level_counts": {"type": "object"},
                    "source_linked_entry_count": {"type": "integer"},
                    "asset_materialized_entry_count": {"type": "integer"},
                    "static_certified_release_task_count": {"type": "integer"},
                    "dual_certified_release_task_count": {"type": "integer"},
                    "scored_release_entries": {"type": "integer"},
                    "scored_release_forms": {"type": "integer"},
                    "score_denominator_status": {"type": "string"},
                    "claim_status": {"type": "string"},
                },
            },
            "parity_summary": {
                "type": "object",
                "required": [
                    "release_dual_status",
                    "dual_certified_release_task_count",
                    "dual_pending_release_task_count",
                    "dual_failed_release_task_count",
                    "evas_pass_spectre_fail_count",
                    "l0_conformance_case_count",
                    "l0_counts_in_benchmark_denominator",
                    "dual_rerun_staging_status",
                    "latest_dual_rerun_attempt_status",
                    "bridge_diagnostics_status",
                ],
                "properties": {
                    "release_dual_status": {"type": "string"},
                    "dual_certified_release_task_count": {"type": "integer"},
                    "dual_pending_release_task_count": {"type": "integer"},
                    "dual_failed_release_task_count": {"type": "integer"},
                    "evas_pass_spectre_fail_count": {"type": "integer"},
                    "l0_conformance_case_count": {"type": "integer"},
                    "l0_counts_in_benchmark_denominator": {"type": "integer"},
                    "dual_rerun_staging_status": {"type": "string"},
                    "latest_dual_rerun_attempt_status": {"type": "string"},
                    "bridge_diagnostics_status": {"type": "string"},
                },
            },
            "speed_debug_summary": {
                "type": "object",
                "required": ["status", "claim_allowed", "required_artifact"],
                "properties": {
                    "status": {"type": "string"},
                    "claim_allowed": {"type": "boolean"},
                    "required_artifact": {"type": "string"},
                },
            },
            "baseline_summary": {
                "type": "object",
                "required": [
                    "status",
                    "claim_allowed",
                    "required_artifact",
                    "current_scored_release_entries",
                    "current_scored_release_forms",
                    "score_denominator_status",
                ],
                "properties": {
                    "status": {"type": "string"},
                    "claim_allowed": {"type": "boolean"},
                    "required_artifact": {"type": "string"},
                    "current_scored_release_entries": {"type": "integer"},
                    "current_scored_release_forms": {"type": "integer"},
                    "score_denominator_status": {"type": "string"},
                },
            },
            "certification_gap_summary": {
                "type": "object",
                "required": [
                    "assets_materialized",
                    "static_certification_complete",
                    "fresh_dual_rerun_queue_ready",
                    "dual_pending_release_task_count",
                    "bridge_ready",
                    "external_blockers_status",
                    "stale_rerun_summary_rejected",
                    "import_status",
                ],
                "properties": {
                    "assets_materialized": {"type": "boolean"},
                    "static_certification_complete": {"type": "boolean"},
                    "fresh_dual_rerun_queue_ready": {"type": "boolean"},
                    "dual_pending_release_task_count": {"type": "integer"},
                    "bridge_ready": {"type": "boolean"},
                    "external_blockers_status": {"type": "string"},
                    "stale_rerun_summary_rejected": {"type": "boolean"},
                    "import_status": {"type": "string"},
                },
            },
            "claim_gates": {
                "type": "object",
                "required": [
                    "can_claim_release_assets_materialized",
                    "can_claim_top_level_coverage_plan",
                    "can_claim_release_package_complete",
                    "can_claim_scored_benchmark",
                    "can_claim_zero_evas_pass_spectre_fail_on_imported_release_evidence",
                    "can_claim_speedup",
                    "can_claim_model_baseline",
                    "blocking_conditions",
                ],
                "properties": {
                    "can_claim_release_assets_materialized": {"type": "boolean"},
                    "can_claim_top_level_coverage_plan": {"type": "boolean"},
                    "can_claim_release_package_complete": {"type": "boolean"},
                    "can_claim_scored_benchmark": {"type": "boolean"},
                    "can_claim_zero_evas_pass_spectre_fail_on_imported_release_evidence": {"type": "boolean"},
                    "can_claim_speedup": {"type": "boolean"},
                    "can_claim_model_baseline": {"type": "boolean"},
                    "blocking_conditions": {"type": "array", "items": {"type": "string"}},
                },
            },
            "evidence_sources": {"type": "object"},
            "remaining_counts": {"type": "object"},
        },
        "additionalProperties": True,
    }
    claim_gate_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "vaBench paper claim gate",
        "type": "object",
        "required": [
            "date",
            "release",
            "status",
            "claim_count",
            "allowed_claim_count",
            "blocked_claim_count",
            "completion_required_claim_count",
            "blocked_completion_required_claim_count",
            "claims",
            "blocked_claim_ids",
            "blocked_completion_required_claim_ids",
            "claim_policy",
            "source_reports",
        ],
        "properties": {
            "date": {"type": "string"},
            "release": {"const": "vabench-release-v1"},
            "status": {"enum": ["in_progress", "complete"]},
            "claim_count": {"type": "integer"},
            "allowed_claim_count": {"type": "integer"},
            "blocked_claim_count": {"type": "integer"},
            "completion_required_claim_count": {"type": "integer"},
            "blocked_completion_required_claim_count": {"type": "integer"},
            "claims": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": [
                        "id",
                        "status",
                        "allowed",
                        "completion_required",
                        "claim_text",
                        "safe_wording",
                        "unsafe_wording",
                        "evidence",
                        "required_before_allowed",
                        "numbers",
                        "notes",
                    ],
                    "properties": {
                        "id": {"type": "string"},
                        "status": {"enum": ["allowed", "blocked"]},
                        "allowed": {"type": "boolean"},
                        "completion_required": {"type": "boolean"},
                        "claim_text": {"type": "string"},
                        "safe_wording": {"type": "string"},
                        "unsafe_wording": {"type": "array", "items": {"type": "string"}},
                        "evidence": {"type": "array", "items": {"type": "string"}},
                        "required_before_allowed": {"type": "array", "items": {"type": "string"}},
                        "numbers": {"type": "object"},
                        "notes": {"type": "array", "items": {"type": "string"}},
                    },
                    "additionalProperties": True,
                },
            },
            "blocked_claim_ids": {"type": "array", "items": {"type": "string"}},
            "blocked_completion_required_claim_ids": {"type": "array", "items": {"type": "string"}},
            "claim_policy": {"type": "array", "items": {"type": "string"}},
            "source_reports": {
                "type": "object",
                "required": [
                    "release_status",
                    "dual_certification",
                    "paper_artifacts",
                    "score_denominator_manifest",
                    "speed_debug_artifact",
                    "baseline_artifact",
                ],
            },
        },
        "additionalProperties": True,
    }
    score_denominator_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "vaBench score denominator manifest",
        "type": "object",
        "required": [
            "date",
            "release",
            "status",
            "summary",
            "claim_rule",
            "entry_rows",
            "form_rows",
            "evidence_sources",
        ],
        "properties": {
            "date": {"type": "string"},
            "release": {"const": "vabench-release-v1"},
            "status": {"enum": ["disabled_until_full_certification", "score_enabled"]},
            "summary": {
                "type": "object",
                "required": [
                    "planned_entry_count",
                    "release_form_count",
                    "certified_entry_count",
                    "certified_form_count",
                    "benchmark_score_enabled_entry_count",
                    "benchmark_score_enabled_form_count",
                    "scored_entry_count",
                    "scored_form_count",
                    "l0_conformance_counted_in_denominator",
                    "entry_exclusion_reason_counts",
                    "form_exclusion_reason_counts",
                ],
                "properties": {
                    "planned_entry_count": {"type": "integer"},
                    "release_form_count": {"type": "integer"},
                    "certified_entry_count": {"type": "integer"},
                    "certified_form_count": {"type": "integer"},
                    "benchmark_score_enabled_entry_count": {"type": "integer"},
                    "benchmark_score_enabled_form_count": {"type": "integer"},
                    "scored_entry_count": {"type": "integer"},
                    "scored_form_count": {"type": "integer"},
                    "l0_conformance_counted_in_denominator": {"type": "integer"},
                    "entry_exclusion_reason_counts": {"type": "object"},
                    "form_exclusion_reason_counts": {"type": "object"},
                },
            },
            "claim_rule": {
                "type": "object",
                "required": ["source_of_truth", "denominator_policy", "score_claim_allowed"],
                "properties": {
                    "source_of_truth": {"type": "string"},
                    "denominator_policy": {"type": "string"},
                    "score_claim_allowed": {"type": "boolean"},
                },
            },
            "entry_rows": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": [
                        "release_entry_id",
                        "level",
                        "category",
                        "base_function",
                        "score_surface",
                        "required_forms",
                        "missing_forms",
                        "release_blockers",
                        "manifest",
                        "certified",
                        "benchmark_score_enabled",
                        "counted_in_score",
                        "exclusion_reasons",
                    ],
                    "properties": {
                        "release_entry_id": {"type": "string"},
                        "level": {"enum": ["L1", "L2"]},
                        "category": {"type": "string"},
                        "base_function": {"type": "string"},
                        "score_surface": {"type": "string"},
                        "required_forms": {"type": "array", "items": {"type": "string"}},
                        "missing_forms": {"type": "array", "items": {"type": "string"}},
                        "release_blockers": {"type": "array", "items": {"type": "string"}},
                        "manifest": {"type": "string"},
                        "certified": {"type": "boolean"},
                        "benchmark_score_enabled": {"type": "boolean"},
                        "counted_in_score": {"type": "boolean"},
                        "exclusion_reasons": {"type": "array", "items": {"type": "string"}},
                    },
                },
            },
            "form_rows": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": [
                        "release_entry_id",
                        "task_id",
                        "form",
                        "level",
                        "category",
                        "base_function",
                        "score_surface",
                        "manifest",
                        "static",
                        "evas",
                        "spectre",
                        "certified",
                        "benchmark_score_enabled",
                        "counted_in_score",
                        "exclusion_reasons",
                    ],
                    "properties": {
                        "release_entry_id": {"type": "string"},
                        "task_id": {"type": "string"},
                        "form": {"enum": ["dut", "tb", "bugfix", "e2e"]},
                        "level": {"enum": ["L1", "L2"]},
                        "category": {"type": "string"},
                        "base_function": {"type": "string"},
                        "score_surface": {"type": "string"},
                        "manifest": {"type": "string"},
                        "static": {"enum": ["pending", "pass", "fail"]},
                        "evas": {"enum": ["pending", "pass", "fail"]},
                        "spectre": {"enum": ["pending", "pass", "fail"]},
                        "certified": {"type": "boolean"},
                        "benchmark_score_enabled": {"type": "boolean"},
                        "counted_in_score": {"type": "boolean"},
                        "exclusion_reasons": {"type": "array", "items": {"type": "string"}},
                    },
                },
            },
            "evidence_sources": {"type": "object"},
        },
        "additionalProperties": True,
    }
    dual_rerun_queue_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "vaBench dual rerun queue",
        "type": "object",
        "required": [
            "date",
            "release",
            "status",
            "queue_count",
            "reason_counts",
            "form_counts",
            "ready_count",
            "blocked_count",
            "rows",
            "notes",
        ],
        "properties": {
            "date": {"type": "string"},
            "release": {"const": "vabench-release-v1"},
            "status": {"enum": ["ready", "blocked"]},
            "queue_count": {"type": "integer"},
            "reason_counts": {"type": "object"},
            "form_counts": {"type": "object"},
            "ready_count": {"type": "integer"},
            "blocked_count": {"type": "integer"},
            "rows": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": [
                        "entry_id",
                        "form",
                        "level",
                        "category",
                        "base_function",
                        "source_task_id",
                        "queue_reason",
                        "static_status",
                        "evas_status",
                        "spectre_status",
                        "gold",
                        "evidence",
                        "pending_blockers",
                        "ready_for_dual_rerun",
                    ],
                    "properties": {
                        "entry_id": {"type": "string"},
                        "form": {"enum": ["dut", "tb", "bugfix", "e2e"]},
                        "level": {"enum": ["L1", "L2"]},
                        "category": {"type": "string"},
                        "base_function": {"type": "string"},
                        "source_task_id": {"type": "string"},
                        "queue_reason": {"type": "string"},
                        "static_status": {"enum": ["pending", "pass", "fail", "missing"]},
                        "evas_status": {"enum": ["pending", "pass", "fail", "missing"]},
                        "spectre_status": {"enum": ["pending", "pass", "fail", "missing"]},
                        "gold": {"type": "array", "items": {"type": "string"}},
                        "evidence": {"type": "string"},
                        "pending_blockers": {"type": "array", "items": {"type": "string"}},
                        "ready_for_dual_rerun": {"type": "boolean"},
                    },
                    "additionalProperties": True,
                },
            },
            "notes": {"type": "array", "items": {"type": "string"}},
        },
        "additionalProperties": True,
    }
    dual_rerun_staging_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "vaBench dual rerun staging manifest",
        "type": "object",
        "required": [
            "date",
            "release",
            "status",
            "queue_row_count",
            "queue_rows_with_ready_primary_bundle",
            "bundle_count",
            "ready_bundle_count",
            "blocked_bundle_count",
            "form_counts",
            "variant_counts",
            "blocker_counts",
            "staging_root",
            "bundles",
            "notes",
        ],
        "properties": {
            "date": {"type": "string"},
            "release": {"const": "vabench-release-v1"},
            "status": {"enum": ["ready", "blocked"]},
            "queue_row_count": {"type": "integer"},
            "queue_rows_with_ready_primary_bundle": {"type": "integer"},
            "bundle_count": {"type": "integer"},
            "ready_bundle_count": {"type": "integer"},
            "blocked_bundle_count": {"type": "integer"},
            "form_counts": {"type": "object"},
            "variant_counts": {"type": "object"},
            "blocker_counts": {"type": "object"},
            "staging_root": {"type": "string"},
            "bundles": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": [
                        "entry_id",
                        "form",
                        "variant",
                        "expected_result",
                        "source_task_id",
                        "queue_reason",
                        "status",
                        "blockers",
                        "staged_task_dir",
                        "staged_gold_dir",
                        "source_testbench",
                        "source_includes",
                        "source_include_origins",
                        "staged_testbench",
                        "staged_includes",
                    ],
                    "properties": {
                        "entry_id": {"type": "string"},
                        "form": {"enum": ["dut", "tb", "bugfix", "e2e"]},
                        "variant": {"enum": ["gold", "fixed", "buggy"]},
                        "expected_result": {"enum": ["pass", "fail"]},
                        "source_task_id": {"type": "string"},
                        "queue_reason": {"type": "string"},
                        "status": {"enum": ["ready", "blocked"]},
                        "blockers": {"type": "array", "items": {"type": "string"}},
                        "staged_task_dir": {"type": "string"},
                        "staged_gold_dir": {"type": "string"},
                        "source_testbench": {"type": "string"},
                        "source_includes": {"type": "array", "items": {"type": "string"}},
                        "source_include_origins": {"type": "object"},
                        "staged_testbench": {"type": "string"},
                        "staged_includes": {"type": "array", "items": {"type": "string"}},
                    },
                    "additionalProperties": True,
                },
            },
            "notes": {"type": "array", "items": {"type": "string"}},
        },
        "additionalProperties": True,
    }
    dual_rerun_import_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "vaBench dual rerun import report",
        "type": "object",
        "required": [
            "date",
            "status",
            "reason",
            "summary",
            "current_queue_count",
            "summary_tasks_total",
            "stale_summary",
            "imported_primary_result_count",
            "notes",
        ],
        "properties": {
            "date": {"type": "string"},
            "release": {"const": "vabench-release-v1"},
            "status": {"enum": ["imported", "imported_with_failures", "blocked", "missing"]},
            "reason": {"type": "string"},
            "summary": {"type": "string"},
            "tasks_total": {"type": "integer"},
            "current_queue_count": {"type": "integer"},
            "summary_tasks_total": {"type": "integer"},
            "stale_summary": {"type": "boolean"},
            "imported_primary_result_count": {"type": "integer"},
            "notes": {"type": "array", "items": {"type": "string"}},
        },
        "additionalProperties": True,
    }
    bridge_diagnostics_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "vaBench bridge diagnostics",
        "type": "object",
        "required": [
            "date",
            "release",
            "status",
            "reason",
            "bridge_repo",
            "profile_count",
            "ready_profiles",
            "ssh_ok_profiles",
            "ssh_failure_code_counts",
            "hop_ssh_failure_code_counts",
            "ssh_timeout_s",
            "skip_ssh",
            "profiles",
            "notes",
        ],
        "properties": {
            "date": {"type": "string"},
            "release": {"const": "vabench-release-v1"},
            "status": {"enum": ["ready", "blocked"]},
            "reason": {"type": "string"},
            "bridge_repo": {"type": "string"},
            "profile_count": {"type": "integer"},
            "ready_profiles": {"type": "array", "items": {"type": "string"}},
            "ssh_ok_profiles": {"type": "array", "items": {"type": "string"}},
            "ssh_config_jump_ok_profiles": {"type": "array", "items": {"type": "string"}},
            "ssh_failure_code_counts": {"type": "object"},
            "alternate_ssh_failure_code_counts": {"type": "object"},
            "hop_ssh_failure_code_counts": {"type": "object"},
            "hop_ssh_ok_routes": {"type": "array", "items": {"type": "string"}},
            "ssh_timeout_s": {"type": "integer"},
            "skip_ssh": {"type": "boolean"},
            "profiles": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": [
                        "profile",
                        "remote_host",
                        "remote_user",
                        "local_port",
                        "diagnostic_notes",
                        "hop_ssh_smokes",
                        "ssh_smoke",
                        "alternate_ssh_smokes",
                        "preflight",
                        "ready_for_release_rerun",
                    ],
                    "properties": {
                        "profile": {"type": "string"},
                        "remote_host": {"type": "string"},
                        "remote_user": {"type": "string"},
                        "local_port": {"type": "integer"},
                        "use_ssh_config_jump": {"type": "boolean"},
                        "diagnostic_notes": {"type": "array", "items": {"type": "string"}},
                        "hop_ssh_smokes": {"type": "array", "items": {"type": "object"}},
                        "ssh_smoke": {"type": "object"},
                        "alternate_ssh_smokes": {"type": "array", "items": {"type": "object"}},
                        "preflight": {"type": "object"},
                        "ready_for_release_rerun": {"type": "boolean"},
                    },
                    "additionalProperties": True,
                },
            },
            "notes": {"type": "array", "items": {"type": "string"}},
        },
        "additionalProperties": True,
    }
    external_blockers_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "vaBench external blocker report",
        "type": "object",
        "required": [
            "date",
            "release",
            "status",
            "blocker_count",
            "blocked_count",
            "pending_count",
            "ready_to_continue_count",
            "bridge_status",
            "queue_count",
            "ready_staging_bundle_count",
            "latest_rerun_summary_status",
            "latest_import_status",
            "paper_status",
            "completion_status",
            "blockers",
            "claim_boundary",
            "recovery_sequence",
        ],
        "properties": {
            "date": {"type": "string"},
            "release": {"const": "vabench-release-v1"},
            "status": {"enum": ["blocked", "pending", "clear"]},
            "blocker_count": {"type": "integer"},
            "blocked_count": {"type": "integer"},
            "pending_count": {"type": "integer"},
            "ready_to_continue_count": {"type": "integer"},
            "bridge_status": {"type": "string"},
            "bridge_reason": {"type": "string"},
            "queue_count": {"type": "integer"},
            "ready_staging_bundle_count": {"type": "integer"},
            "latest_rerun_summary_status": {"type": "string"},
            "latest_import_status": {"type": "string"},
            "paper_status": {"type": "string"},
            "completion_status": {"type": "string"},
            "blockers": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": [
                        "id",
                        "status",
                        "scope",
                        "diagnosis",
                        "claim_impact",
                        "evidence",
                        "recovery_commands",
                        "stop_condition",
                        "details",
                    ],
                    "properties": {
                        "id": {"type": "string"},
                        "status": {"enum": ["blocked", "pending", "ready_to_continue", "clear"]},
                        "scope": {"type": "string"},
                        "diagnosis": {"type": "string"},
                        "claim_impact": {"type": "array", "items": {"type": "string"}},
                        "evidence": {"type": "array", "items": {"type": "string"}},
                        "recovery_commands": {"type": "array", "items": {"type": "string"}},
                        "stop_condition": {"type": "string"},
                        "details": {"type": "object"},
                    },
                    "additionalProperties": True,
                },
            },
            "claim_boundary": {"type": "array", "items": {"type": "string"}},
            "recovery_sequence": {"type": "array", "items": {"type": "string"}},
        },
        "additionalProperties": True,
    }
    finish_readiness_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "vaBench finish readiness gate",
        "type": "object",
        "required": [
            "date",
            "release",
            "status",
            "ready_to_run_fresh_dual",
            "ready_to_import_fresh_dual",
            "ready_to_finish_release",
            "pass_count",
            "blocked_count",
            "blocked_check_ids",
            "run_scope",
            "checks",
            "fresh_summary_acceptance_criteria",
            "next_commands",
            "claim_boundary",
            "evidence_sources",
        ],
        "properties": {
            "date": {"type": "string"},
            "release": {"const": "vabench-release-v1"},
            "status": {"enum": ["blocked", "ready_to_run", "ready_to_finish"]},
            "ready_to_run_fresh_dual": {"type": "boolean"},
            "ready_to_import_fresh_dual": {"type": "boolean"},
            "ready_to_finish_release": {"type": "boolean"},
            "pass_count": {"type": "integer"},
            "blocked_count": {"type": "integer"},
            "blocked_check_ids": {"type": "array", "items": {"type": "string"}},
            "run_scope": {
                "type": "object",
                "required": [
                    "primary_queue_rows",
                    "ready_primary_queue_rows",
                    "staged_bundle_count",
                    "ready_staged_bundle_count",
                    "expected_primary_summary_tasks_total",
                ],
            },
            "checks": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["id", "status", "requirement", "evidence", "finding", "recovery"],
                    "properties": {
                        "id": {"type": "string"},
                        "status": {"enum": ["pass", "blocked"]},
                        "requirement": {"type": "string"},
                        "evidence": {"type": "array", "items": {"type": "string"}},
                        "finding": {"type": "string"},
                        "recovery": {"type": "array", "items": {"type": "string"}},
                    },
                    "additionalProperties": True,
                },
            },
            "fresh_summary_acceptance_criteria": {"type": "array", "items": {"type": "string"}},
            "next_commands": {"type": "object"},
            "claim_boundary": {"type": "array", "items": {"type": "string"}},
            "evidence_sources": {"type": "object"},
        },
        "additionalProperties": True,
    }
    completion_audit_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "vaBench release completion audit",
        "type": "object",
        "required": [
            "date",
            "release",
            "status",
            "proved_count",
            "blocked_count",
            "incomplete_count",
            "requirements",
            "blocking_conditions",
            "next_actions",
            "notes",
            "evidence_sources",
        ],
        "properties": {
            "date": {"type": "string"},
            "release": {"const": "vabench-release-v1"},
            "status": {"enum": ["complete", "in_progress", "blocked"]},
            "proved_count": {"type": "integer"},
            "blocked_count": {"type": "integer"},
            "incomplete_count": {"type": "integer"},
            "requirements": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["id", "requirement", "status", "evidence", "finding", "blockers"],
                    "properties": {
                        "id": {"type": "string"},
                        "requirement": {"type": "string"},
                        "status": {"enum": ["proved", "blocked", "incomplete"]},
                        "evidence": {"type": "array", "items": {"type": "string"}},
                        "finding": {"type": "string"},
                        "blockers": {"type": "array", "items": {"type": "string"}},
                    },
                    "additionalProperties": True,
                },
            },
            "blocking_conditions": {"type": "array", "items": {"type": "string"}},
            "next_actions": {"type": "array", "items": {"type": "string"}},
            "notes": {"type": "array", "items": {"type": "string"}},
            "evidence_sources": {
                "type": "object",
                "required": [
                    "tracker",
                    "release_status",
                    "schema_validation",
                    "package_manifest",
                    "evaluator_contract",
                    "asset_integrity",
                    "static_certification",
                    "dual_certification",
                    "remaining_work",
                    "bridge_profile_diagnostics",
                    "external_blockers",
                    "finish_readiness",
                    "claim_gate",
                    "paper_tables",
                    "paper_artifacts",
                    "score_denominator_manifest",
                ],
            },
        },
        "additionalProperties": True,
    }
    finish_after_bridge_attempt_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "vaBench finish-after-bridge attempt report",
        "type": "object",
        "required": [
            "date",
            "release",
            "status",
            "reason",
            "dry_run",
            "bridge_repo",
            "profiles",
            "bridge_diagnostics_status",
            "bridge_ready_profiles",
            "rerun_scope",
            "output_root",
            "summary",
            "attempts",
            "post_attempt_completion_status",
            "post_attempt_completion_blockers",
            "next_actions",
        ],
        "properties": {
            "date": {"type": "string"},
            "release": {"const": "vabench-release-v1"},
            "status": {"enum": ["complete", "complete_with_failures", "blocked", "dry_run"]},
            "reason": {"type": "string"},
            "dry_run": {"type": "boolean"},
            "bridge_repo": {"type": "string"},
            "profiles": {"type": "array", "items": {"type": "string"}},
            "bridge_diagnostics_status": {"enum": ["ready", "blocked", "missing"]},
            "bridge_diagnostics_reason": {"type": ["string", "null"]},
            "bridge_ready_profiles": {"type": "array", "items": {"type": "string"}},
            "bridge_ssh_ok_profiles": {"type": "array", "items": {"type": "string"}},
            "rerun_scope": {
                "type": "object",
                "required": [
                    "queue_status",
                    "primary_queue_count",
                    "primary_ready_count",
                    "primary_blocked_count",
                    "staging_status",
                    "staging_bundle_count",
                    "staging_ready_bundle_count",
                    "staging_blocked_bundle_count",
                    "include_buggy",
                    "planned_bundle_limit",
                    "latest_summary_status",
                    "latest_import_status",
                    "latest_import_stale_summary",
                ],
                "additionalProperties": True,
            },
            "output_root": {"type": "string"},
            "summary": {"type": "string"},
            "attempts": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["profile", "command"],
                    "properties": {
                        "profile": {"type": "string"},
                        "command": {"type": "array", "items": {"type": "string"}},
                        "status": {"type": "string"},
                        "summary_status": {"type": "string"},
                        "summary_reason": {"type": "string"},
                    },
                    "additionalProperties": True,
                },
            },
            "post_attempt_completion_status": {"type": "string"},
            "post_attempt_completion_blockers": {"type": "array", "items": {"type": "string"}},
            "next_actions": {"type": "array", "items": {"type": "string"}},
        },
        "additionalProperties": True,
    }
    conformance_manifest_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "vaBench L0 EVAS/Spectre conformance manifest",
        "type": "object",
        "required": [
            "date",
            "suite",
            "conformance_case_count",
            "model_capability_count",
            "benchmark_coverage_count",
            "bugfix_claim_count",
            "broad_parity_denominator_count",
            "runner_hook_required_count",
            "cases",
            "notes",
        ],
        "properties": {
            "date": {"type": "string"},
            "suite": {"const": "evas-spectre"},
            "conformance_case_count": {"type": "integer"},
            "model_capability_count": {"const": 0},
            "benchmark_coverage_count": {"const": 0},
            "bugfix_claim_count": {"const": 0},
            "broad_parity_denominator_count": {"const": 0},
            "runner_hook_required_count": {"type": "integer"},
            "cases": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": [
                        "id",
                        "suite",
                        "conformance_axis",
                        "expected_relation",
                        "source_path",
                        "package_path",
                        "model_capability",
                        "benchmark_coverage",
                        "bugfix_claim",
                        "broad_parity_denominator",
                        "runner_hook_required",
                    ],
                    "properties": {
                        "id": {"type": "string"},
                        "suite": {"const": "evas-spectre"},
                        "conformance_axis": {"type": "string"},
                        "expected_relation": {"type": "string"},
                        "source_path": {"type": "string"},
                        "package_path": {"type": "string"},
                        "model_capability": {"enum": [False, "false"]},
                        "benchmark_coverage": {"enum": [False, "false"]},
                        "bugfix_claim": {"enum": [False, "false"]},
                        "broad_parity_denominator": {"enum": [False, "false"]},
                        "runner_hook_required": {"enum": [True, False, "true", "false"]},
                    },
                    "additionalProperties": True,
                },
            },
            "notes": {"type": "array", "items": {"type": "string"}},
        },
        "additionalProperties": True,
    }
    artifact_index_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "vaBench release artifact index",
        "type": "object",
        "required": [
            "date",
            "release",
            "status",
            "artifact_count",
            "missing_artifact_count",
            "missing_artifacts",
            "claim_gates",
            "artifacts",
            "commands",
            "notes",
        ],
        "properties": {
            "date": {"type": "string"},
            "release": {"const": "vabench-release-v1"},
            "status": {"enum": ["complete", "in_progress", "blocked"]},
            "artifact_count": {"type": "integer"},
            "missing_artifact_count": {"type": "integer"},
            "missing_artifacts": {"type": "array", "items": {"type": "object"}},
            "claim_gates": {"type": "object"},
            "artifacts": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": [
                        "id",
                        "path",
                        "exists",
                        "kind",
                        "purpose",
                        "claim_role",
                        "status",
                        "certification_evidence",
                        "notes",
                    ],
                    "properties": {
                        "id": {"type": "string"},
                        "path": {"type": "string"},
                        "exists": {"type": "boolean"},
                        "kind": {"type": "string"},
                        "purpose": {"type": "string"},
                        "claim_role": {"type": "string"},
                        "status": {"type": "string"},
                        "certification_evidence": {"type": "boolean"},
                        "notes": {"type": "array", "items": {"type": "string"}},
                    },
                    "additionalProperties": True,
                },
            },
            "commands": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["id", "command", "purpose"],
                    "properties": {
                        "id": {"type": "string"},
                        "command": {"type": "string"},
                        "purpose": {"type": "string"},
                    },
                    "additionalProperties": True,
                },
            },
            "notes": {"type": "array", "items": {"type": "string"}},
        },
        "additionalProperties": True,
    }
    checksum_manifest_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "vaBench release checksum manifest",
        "type": "object",
        "required": [
            "date",
            "release",
            "status",
            "algorithm",
            "file_count",
            "total_bytes",
            "category_counts",
            "excluded_files",
            "files",
            "notes",
        ],
        "properties": {
            "date": {"type": "string"},
            "release": {"const": "vabench-release-v1"},
            "status": {"enum": ["pass", "fail"]},
            "algorithm": {"const": "sha256"},
            "file_count": {"type": "integer"},
            "total_bytes": {"type": "integer"},
            "category_counts": {"type": "object"},
            "excluded_files": {"type": "array", "items": {"type": "string"}},
            "files": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["path", "category", "bytes", "sha256"],
                    "properties": {
                        "path": {"type": "string"},
                        "category": {"type": "string"},
                        "bytes": {"type": "integer"},
                        "sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
                    },
                    "additionalProperties": True,
                },
            },
            "notes": {"type": "array", "items": {"type": "string"}},
        },
        "additionalProperties": True,
    }
    paper_tables_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "vaBench paper tables report",
        "type": "object",
        "required": [
            "date",
            "release",
            "status",
            "table_count",
            "tables",
            "source_reports",
            "table_rows",
            "claim_boundary",
            "matrix_summary_snapshot",
        ],
        "properties": {
            "date": {"type": "string"},
            "release": {"const": "vabench-release-v1"},
            "status": {"enum": ["complete", "in_progress"]},
            "table_count": {"type": "integer"},
            "tables": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["id", "title", "csv", "row_count", "caption"],
                    "properties": {
                        "id": {"type": "string"},
                        "title": {"type": "string"},
                        "csv": {"type": "string"},
                        "row_count": {"type": "integer"},
                        "caption": {"type": "string"},
                    },
                    "additionalProperties": True,
                },
            },
            "source_reports": {"type": "object"},
            "table_rows": {"type": "object"},
            "claim_boundary": {"type": "array", "items": {"type": "string"}},
            "matrix_summary_snapshot": {"type": "object"},
        },
        "additionalProperties": True,
    }
    release_task_manifest_sync_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "vaBench release task manifest sync report",
        "type": "object",
        "required": ["date", "release", "status", "release_task_manifest_count", "rows", "notes"],
        "properties": {
            "date": {"type": "string"},
            "release": {"const": "vabench-release-v1"},
            "status": {"enum": ["pass", "fail"]},
            "release_task_manifest_count": {"type": "integer"},
            "rows": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["release_entry_id", "form", "manifest", "static", "evas", "spectre"],
                    "properties": {
                        "release_entry_id": {"type": "string"},
                        "form": {"type": "string"},
                        "manifest": {"type": "string"},
                        "static": {"type": "string"},
                        "evas": {"type": "string"},
                        "spectre": {"type": "string"},
                    },
                    "additionalProperties": True,
                },
            },
            "notes": {"type": "array", "items": {"type": "string"}},
        },
        "additionalProperties": True,
    }
    release_status_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "vaBench release status report",
        "type": "object",
        "required": [
            "date",
            "release",
            "planned_entries",
            "level_counts",
            "package_status_counts",
            "tracker_certification_counts",
            "source_linked_entry_count",
            "asset_materialized_entry_count",
            "asset_integrity_status",
            "asset_integrity_issue_count",
            "asset_integrity_warning_count",
            "static_certification_status",
            "static_certified_release_task_count",
            "static_failed_release_task_count",
            "static_certified_entry_count",
            "dual_certification_status",
            "dual_certified_release_task_count",
            "dual_failed_release_task_count",
            "dual_pending_release_task_count",
            "fully_certified_entry_count",
            "source_equivalence_failure_count",
            "source_equivalence_blocked_release_task_count",
            "evas_pass_spectre_fail_count",
            "dual_simulator_rerun",
            "l0_conformance_case_count",
            "scored_release_entries",
            "certified_release_entries",
            "stop_condition",
            "next_actions",
        ],
        "properties": {
            "date": {"type": "string"},
            "release": {"const": "vabench-release-v1"},
            "planned_entries": {"type": "integer"},
            "level_counts": {"type": "object"},
            "package_status_counts": {"type": "object"},
            "tracker_certification_counts": {"type": "object"},
            "source_linked_entry_count": {"type": "integer"},
            "asset_materialized_entry_count": {"type": "integer"},
            "asset_integrity_status": {"enum": ["pass", "fail", "missing"]},
            "asset_integrity_issue_count": {"type": "integer"},
            "asset_integrity_warning_count": {"type": "integer"},
            "static_certification_status": {"enum": ["pass", "fail", "missing"]},
            "static_certified_release_task_count": {"type": "integer"},
            "static_failed_release_task_count": {"type": "integer"},
            "static_certified_entry_count": {"type": "integer"},
            "dual_certification_status": {"enum": ["pass", "partial", "fail", "missing"]},
            "dual_certified_release_task_count": {"type": "integer"},
            "dual_failed_release_task_count": {"type": "integer"},
            "dual_pending_release_task_count": {"type": "integer"},
            "fully_certified_entry_count": {"type": "integer"},
            "source_equivalence_failure_count": {"type": "integer"},
            "source_equivalence_blocked_release_task_count": {"type": "integer"},
            "evas_pass_spectre_fail_count": {"type": "integer"},
            "dual_simulator_rerun": {"type": "boolean"},
            "l0_conformance_case_count": {"type": "integer"},
            "scored_release_entries": {"type": "integer"},
            "certified_release_entries": {"type": "integer"},
            "stop_condition": {"type": ["string", "object"]},
            "next_actions": {"type": "array", "items": {"type": "string"}},
        },
        "additionalProperties": True,
    }
    asset_integrity_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "vaBench release asset integrity report",
        "type": "object",
        "required": [
            "date",
            "release",
            "status",
            "audited_release_task_count",
            "form_counts",
            "issue_count",
            "warning_count",
            "task_reports",
            "notes",
        ],
        "properties": {
            "date": {"type": "string"},
            "release": {"const": "vabench-release-v1"},
            "status": {"enum": ["pass", "fail"]},
            "audited_release_task_count": {"type": "integer"},
            "form_counts": {"type": "object"},
            "issue_count": {"type": "integer"},
            "warning_count": {"type": "integer"},
            "task_reports": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["entry_id", "form", "release_path", "status", "issues", "warnings"],
                    "properties": {
                        "entry_id": {"type": "string"},
                        "form": {"type": "string"},
                        "release_path": {"type": "string"},
                        "status": {"enum": ["pass", "fail"]},
                        "issues": {"type": "array", "items": {"type": "string"}},
                        "warnings": {"type": "array", "items": {"type": "string"}},
                    },
                    "additionalProperties": True,
                },
            },
            "notes": {"type": "array", "items": {"type": "string"}},
        },
        "additionalProperties": True,
    }
    static_certification_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "vaBench release static certification report",
        "type": "object",
        "required": [
            "date",
            "release",
            "status",
            "static_certified_release_task_count",
            "static_failed_release_task_count",
            "static_certified_entry_count",
            "entry_count",
            "issue_count",
            "task_reports",
            "entry_reports",
            "notes",
        ],
        "properties": {
            "date": {"type": "string"},
            "release": {"const": "vabench-release-v1"},
            "status": {"enum": ["pass", "fail"]},
            "static_certified_release_task_count": {"type": "integer"},
            "static_failed_release_task_count": {"type": "integer"},
            "static_certified_entry_count": {"type": "integer"},
            "entry_count": {"type": "integer"},
            "issue_count": {"type": "integer"},
            "task_reports": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": [
                        "entry_id",
                        "form",
                        "task_id",
                        "status",
                        "failure_count",
                        "failures",
                        "evidence",
                        "result",
                    ],
                    "properties": {
                        "entry_id": {"type": "string"},
                        "form": {"type": "string"},
                        "task_id": {"type": "string"},
                        "status": {"enum": ["pass", "fail"]},
                        "failure_count": {"type": "integer"},
                        "failures": {"type": "array", "items": {"type": "string"}},
                        "evidence": {"type": "string"},
                        "result": {"type": "string"},
                    },
                    "additionalProperties": True,
                },
            },
            "entry_reports": {"type": "array", "items": {"type": "object"}},
            "notes": {"type": "array", "items": {"type": "string"}},
        },
        "additionalProperties": True,
    }
    dual_certification_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "vaBench release EVAS/Spectre dual certification report",
        "type": "object",
        "required": [
            "date",
            "release",
            "status",
            "source",
            "simulator_rerun",
            "dual_certified_release_task_count",
            "dual_failed_release_task_count",
            "dual_pending_release_task_count",
            "dual_pass_materialized_entry_count",
            "dual_pending_materialized_entry_count",
            "dual_failed_materialized_entry_count",
            "fully_certified_entry_count",
            "entry_count",
            "issue_count",
            "source_equivalence_failure_count",
            "source_equivalence_blocked_release_task_count",
            "evas_pass_spectre_fail_count",
            "task_reports",
            "entry_reports",
            "notes",
        ],
        "properties": {
            "date": {"type": "string"},
            "release": {"const": "vabench-release-v1"},
            "status": {"enum": ["pass", "partial", "fail"]},
            "source": {"type": "string"},
            "simulator_rerun": {"type": "boolean"},
            "dual_certified_release_task_count": {"type": "integer"},
            "dual_failed_release_task_count": {"type": "integer"},
            "dual_pending_release_task_count": {"type": "integer"},
            "dual_pass_materialized_entry_count": {"type": "integer"},
            "dual_pending_materialized_entry_count": {"type": "integer"},
            "dual_failed_materialized_entry_count": {"type": "integer"},
            "fully_certified_entry_count": {"type": "integer"},
            "entry_count": {"type": "integer"},
            "issue_count": {"type": "integer"},
            "source_equivalence_failure_count": {"type": "integer"},
            "source_equivalence_blocked_release_task_count": {"type": "integer"},
            "evas_pass_spectre_fail_count": {"type": "integer"},
            "task_reports": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": [
                        "entry_id",
                        "form",
                        "source_task_id",
                        "status",
                        "backend_status",
                        "failure_count",
                        "source_equivalence_failure_count",
                        "blocker_count",
                        "failures",
                        "pending_blockers",
                        "evidence",
                    ],
                    "properties": {
                        "entry_id": {"type": "string"},
                        "form": {"type": "string"},
                        "source_task_id": {"type": "string"},
                        "status": {"enum": ["pass", "pending", "fail"]},
                        "backend_status": {"type": "object"},
                        "failure_count": {"type": "integer"},
                        "source_equivalence_failure_count": {"type": "integer"},
                        "blocker_count": {"type": "integer"},
                        "failures": {"type": "array", "items": {"type": "string"}},
                        "pending_blockers": {"type": "array", "items": {"type": "string"}},
                        "evidence": {"type": ["string", "object"]},
                    },
                    "additionalProperties": True,
                },
            },
            "entry_reports": {"type": "array", "items": {"type": "object"}},
            "notes": {"type": "array", "items": {"type": "string"}},
        },
        "additionalProperties": True,
    }
    certification_matrix_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "vaBench release certification matrix",
        "type": "object",
        "required": [
            "date",
            "release",
            "status",
            "summary",
            "source_equivalence_blocked_forms",
            "fresh_dual_rerun_pending_sample",
            "entry_rows",
            "form_rows",
            "claim_boundary",
            "evidence_sources",
        ],
        "properties": {
            "date": {"type": "string"},
            "release": {"const": "vabench-release-v1"},
            "status": {"enum": ["complete", "partial", "blocked"]},
            "summary": {
                "type": "object",
                "required": [
                    "entry_count",
                    "form_count",
                    "fully_certified_entry_count",
                    "pending_entry_count",
                    "certified_form_count",
                    "pending_form_count",
                    "fresh_dual_rerun_pending_form_count",
                    "source_equivalence_blocked_form_count",
                    "dual_failure_form_count",
                    "evas_pass_spectre_fail_count",
                    "scored_entry_count",
                    "scored_form_count",
                ],
                "properties": {
                    "entry_count": {"type": "integer"},
                    "form_count": {"type": "integer"},
                    "fully_certified_entry_count": {"type": "integer"},
                    "pending_entry_count": {"type": "integer"},
                    "certified_form_count": {"type": "integer"},
                    "pending_form_count": {"type": "integer"},
                    "fresh_dual_rerun_pending_form_count": {"type": "integer"},
                    "source_equivalence_blocked_form_count": {"type": "integer"},
                    "dual_failure_form_count": {"type": "integer"},
                    "evas_pass_spectre_fail_count": {"type": "integer"},
                    "scored_entry_count": {"type": "integer"},
                    "scored_form_count": {"type": "integer"},
                },
                "additionalProperties": True,
            },
            "source_equivalence_blocked_forms": {"type": "array", "items": {"type": "object"}},
            "fresh_dual_rerun_pending_sample": {"type": "array", "items": {"type": "object"}},
            "entry_rows": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": [
                        "release_entry_id",
                        "level",
                        "category",
                        "base_function",
                        "package_status",
                        "form_count",
                        "certified_form_count",
                        "pending_form_count",
                        "entry_status",
                        "benchmark_score_enabled",
                        "counted_in_score",
                    ],
                    "additionalProperties": True,
                },
            },
            "form_rows": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": [
                        "release_entry_id",
                        "form",
                        "level",
                        "category",
                        "base_function",
                        "static",
                        "evas",
                        "spectre",
                        "dual_status",
                        "pending_cause",
                        "benchmark_score_enabled",
                        "counted_in_score",
                        "evidence",
                        "release_path",
                    ],
                    "additionalProperties": True,
                },
            },
            "claim_boundary": {"type": "array", "items": {"type": "string"}},
            "evidence_sources": {"type": "object"},
        },
        "additionalProperties": True,
    }
    remaining_work_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "vaBench release remaining work report",
        "type": "object",
        "required": [
            "date",
            "release",
            "status",
            "ready_to_score",
            "planned_entries",
            "source_linked_entry_count",
            "asset_materialized_entry_count",
            "static_certified_release_task_count",
            "dual_certified_release_task_count",
            "dual_pending_release_task_count",
            "dual_failed_release_task_count",
            "evas_pass_spectre_fail_count",
            "scored_release_entries",
            "source_design_pending_entry_count",
            "selected_rerun_pending_form_count",
            "source_equivalence_blocked_form_count",
            "fresh_dual_rerun_queue_form_count",
            "source_equivalence_resolution_policy",
            "missing_required_form_entry_count",
            "current_seed_missing_form_entry_count",
            "source_design_pending_entries",
            "selected_rerun_pending_forms",
            "source_equivalence_blocked_forms",
            "missing_required_form_entries",
            "current_seed_missing_forms",
            "next_queue",
        ],
        "properties": {
            "date": {"type": "string"},
            "release": {"const": "vabench-release-v1"},
            "status": {"enum": ["in_progress", "complete"]},
            "ready_to_score": {"type": "boolean"},
            "planned_entries": {"type": "integer"},
            "source_linked_entry_count": {"type": "integer"},
            "asset_materialized_entry_count": {"type": "integer"},
            "static_certified_release_task_count": {"type": "integer"},
            "dual_certified_release_task_count": {"type": "integer"},
            "dual_pending_release_task_count": {"type": "integer"},
            "dual_failed_release_task_count": {"type": "integer"},
            "evas_pass_spectre_fail_count": {"type": "integer"},
            "scored_release_entries": {"type": "integer"},
            "source_design_pending_entry_count": {"type": "integer"},
            "selected_rerun_pending_form_count": {"type": "integer"},
            "source_equivalence_blocked_form_count": {"type": "integer"},
            "fresh_dual_rerun_queue_form_count": {"type": "integer"},
            "source_equivalence_resolution_policy": {"type": "string"},
            "missing_required_form_entry_count": {"type": "integer"},
            "current_seed_missing_form_entry_count": {"type": "integer"},
            "source_design_pending_entries": {"type": "array", "items": {"type": "object"}},
            "selected_rerun_pending_forms": {"type": "array", "items": {"type": "object"}},
            "source_equivalence_blocked_forms": {"type": "array", "items": {"type": "object"}},
            "missing_required_form_entries": {"type": "array", "items": {"type": "object"}},
            "current_seed_missing_forms": {"type": "array", "items": {"type": "object"}},
            "next_queue": {"type": "array", "items": {"type": "string"}},
        },
        "additionalProperties": True,
    }
    EVALUATOR_CONTRACT_SCHEMA.write_text(json.dumps(evaluator_contract_schema, indent=2) + "\n", encoding="utf-8")
    SPEED_DEBUG_ARTIFACT_SCHEMA.write_text(json.dumps(speed_debug_artifact_schema, indent=2) + "\n", encoding="utf-8")
    BASELINE_ARTIFACT_SCHEMA.write_text(json.dumps(baseline_artifact_schema, indent=2) + "\n", encoding="utf-8")
    PAPER_ARTIFACTS_SCHEMA.write_text(json.dumps(paper_artifacts_schema, indent=2) + "\n", encoding="utf-8")
    CLAIM_GATE_SCHEMA.write_text(json.dumps(claim_gate_schema, indent=2) + "\n", encoding="utf-8")
    SCORE_DENOMINATOR_SCHEMA.write_text(json.dumps(score_denominator_schema, indent=2) + "\n", encoding="utf-8")
    DUAL_RERUN_QUEUE_SCHEMA.write_text(json.dumps(dual_rerun_queue_schema, indent=2) + "\n", encoding="utf-8")
    DUAL_RERUN_STAGING_SCHEMA.write_text(json.dumps(dual_rerun_staging_schema, indent=2) + "\n", encoding="utf-8")
    DUAL_RERUN_IMPORT_SCHEMA.write_text(json.dumps(dual_rerun_import_schema, indent=2) + "\n", encoding="utf-8")
    BRIDGE_DIAGNOSTICS_SCHEMA.write_text(json.dumps(bridge_diagnostics_schema, indent=2) + "\n", encoding="utf-8")
    EXTERNAL_BLOCKERS_SCHEMA.write_text(json.dumps(external_blockers_schema, indent=2) + "\n", encoding="utf-8")
    FINISH_READINESS_SCHEMA.write_text(json.dumps(finish_readiness_schema, indent=2) + "\n", encoding="utf-8")
    COMPLETION_AUDIT_SCHEMA.write_text(json.dumps(completion_audit_schema, indent=2) + "\n", encoding="utf-8")
    FINISH_AFTER_BRIDGE_ATTEMPT_SCHEMA.write_text(json.dumps(finish_after_bridge_attempt_schema, indent=2) + "\n", encoding="utf-8")
    CONFORMANCE_MANIFEST_SCHEMA.write_text(json.dumps(conformance_manifest_schema, indent=2) + "\n", encoding="utf-8")
    ARTIFACT_INDEX_SCHEMA.write_text(json.dumps(artifact_index_schema, indent=2) + "\n", encoding="utf-8")
    CHECKSUM_MANIFEST_SCHEMA.write_text(json.dumps(checksum_manifest_schema, indent=2) + "\n", encoding="utf-8")
    PAPER_TABLES_SCHEMA.write_text(json.dumps(paper_tables_schema, indent=2) + "\n", encoding="utf-8")
    RELEASE_TASK_MANIFEST_SYNC_SCHEMA.write_text(json.dumps(release_task_manifest_sync_schema, indent=2) + "\n", encoding="utf-8")
    RELEASE_STATUS_SCHEMA.write_text(json.dumps(release_status_schema, indent=2) + "\n", encoding="utf-8")
    ASSET_INTEGRITY_SCHEMA.write_text(json.dumps(asset_integrity_schema, indent=2) + "\n", encoding="utf-8")
    STATIC_CERTIFICATION_SCHEMA.write_text(json.dumps(static_certification_schema, indent=2) + "\n", encoding="utf-8")
    DUAL_CERTIFICATION_SCHEMA.write_text(json.dumps(dual_certification_schema, indent=2) + "\n", encoding="utf-8")
    CERTIFICATION_MATRIX_SCHEMA.write_text(json.dumps(certification_matrix_schema, indent=2) + "\n", encoding="utf-8")
    REMAINING_WORK_SCHEMA.write_text(json.dumps(remaining_work_schema, indent=2) + "\n", encoding="utf-8")
    PACKAGE_MANIFEST_SCHEMA.write_text(json.dumps(package_manifest_schema, indent=2) + "\n", encoding="utf-8")
    RELEASE_ENTRY_SCHEMA.write_text(json.dumps(release_entry_schema, indent=2) + "\n", encoding="utf-8")
    RELEASE_TASK_SCHEMA.write_text(json.dumps(release_task_schema, indent=2) + "\n", encoding="utf-8")
    EVIDENCE_SCHEMA.write_text(json.dumps(evidence_schema, indent=2) + "\n", encoding="utf-8")
    RESULT_SCHEMA.write_text(json.dumps(result_schema, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    rows = parse_release_rows()
    if len(rows) != 75:
        raise SystemExit(f"expected 75 release rows, found {len(rows)}")
    write_goal()
    write_tracker(rows)
    write_package_readme()
    write_schemas()
    print(f"initialized vaBench release goal with {len(rows)} rows")


if __name__ == "__main__":
    main()
