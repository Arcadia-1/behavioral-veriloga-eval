#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SPEED_OPT_ROOT = ROOT / "speed-optimization"
REPORTS_ROOT = SPEED_OPT_ROOT / "reports"

DEFAULT_COVERAGE_JSON = REPORTS_ROOT / "current_release_rust_coverage_manifest_20260604.json"
DEFAULT_STAGE_JSON = REPORTS_ROOT / "rust_stage55_topwall10_072_20260604.json"
DEFAULT_REPORT_JSON = REPORTS_ROOT / "rust_speed_claim_gate_073_20260604.json"
DEFAULT_REPORT_MD = REPORTS_ROOT / "rust_speed_claim_gate_073_20260604.md"

SCHEMA_VERSION = "evas-rust-speed-claim-gate.v1"

PRODUCTION_STATUS = {"implemented"}
DEFAULT_MIN_STAGE_COMPLETION = 0.55
DEFAULT_FULL_RUST_PERCENT = 99.9


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def read_json(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def float_or_none(value: object) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def bool_true(value: object) -> bool:
    return value is True or str(value).strip().lower() == "true"


def build_stage_gate(stage: dict[str, Any], *, min_completion: float) -> dict[str, Any]:
    blockers: list[str] = []
    topwall = stage.get("topwall10_evas_only", {})
    if not isinstance(topwall, dict):
        topwall = {}
        blockers.append("missing_topwall10_evas_only")

    rows = int(topwall.get("rows", 0) or 0)
    normal_passes = int(topwall.get("normal_fast_passes", 0) or 0)
    rust_passes = int(topwall.get("rust55_passes", 0) or 0)
    completion = float_or_none(topwall.get("topwall_weighted_completion")) or 0.0
    speedup = float_or_none(topwall.get("total_wall_speedup"))

    if rows <= 0:
        blockers.append("no_stage_rows")
    if normal_passes != rows or rust_passes != rows:
        blockers.append("stage_rows_not_all_pass")
    if completion < min_completion:
        blockers.append("stage_completion_below_threshold")
    if speedup is None or speedup <= 1.0:
        blockers.append("stage_wall_speedup_not_positive")

    return {
        "claim": "stage55_topwall_engineering_speedup",
        "allowed": not blockers,
        "scope": "EVAS-only top-wall engineering slice",
        "threshold": min_completion,
        "observed_completion": completion,
        "observed_completion_percent": round(100.0 * completion, 1),
        "rows": rows,
        "normal_fast_passes": normal_passes,
        "rust55_passes": rust_passes,
        "total_wall_speedup": speedup,
        "blockers": blockers,
    }


def build_full_rust_gate(
    coverage: dict[str, Any],
    *,
    full_rust_percent: float,
) -> dict[str, Any]:
    blockers: list[str] = []
    estimate = coverage.get("rustification_completion_estimate", {})
    if not isinstance(estimate, dict):
        estimate = {}
    percent = float_or_none(estimate.get("percent")) or 0.0
    summary = coverage.get("summary", {})
    if not isinstance(summary, dict):
        summary = {}
    model_rows = int(summary.get("model_rows", 0) or 0)
    invalid_candidates = int(summary.get("whole_segment_invalid_candidate_count", 0) or 0)

    behavior_blockers: list[dict[str, Any]] = []
    for row in coverage.get("behavior_table", []) or []:
        if not isinstance(row, dict):
            continue
        present_rows = int(row.get("present_model_rows", 0) or 0)
        status = str(row.get("current_status", "not_implemented"))
        if present_rows > 0 and status not in PRODUCTION_STATUS:
            behavior_blockers.append(
                {
                    "id": row.get("id"),
                    "name": row.get("name", ""),
                    "status": status,
                    "present_model_rows": present_rows,
                    "rust_primitive": row.get("rust_primitive"),
                    "fallback_reasons": row.get("fallback_reasons", []),
                }
            )

    if not coverage:
        blockers.append("missing_release_rust_coverage_manifest")
    if model_rows <= 0:
        blockers.append("no_release_models_scanned")
    if percent < full_rust_percent:
        blockers.append("release_rustification_percent_below_full_threshold")
    if behavior_blockers:
        blockers.append("non_production_behavior_status_present")
    if invalid_candidates:
        blockers.append("invalid_whole_segment_candidates_present")

    return {
        "claim": "full_release_rustification",
        "allowed": not blockers,
        "scope": "release-wide Verilog-A semantic coverage",
        "threshold_percent": full_rust_percent,
        "observed_percent": percent,
        "model_rows": model_rows,
        "whole_segment_invalid_candidate_count": invalid_candidates,
        "behavior_blocker_count": len(behavior_blockers),
        "behavior_blockers": behavior_blockers[:20],
        "blockers": blockers,
    }


def mode_summary_rows(report: dict[str, Any]) -> list[dict[str, Any]]:
    summary = report.get("summary", {})
    if isinstance(summary, dict):
        rows = summary.get("mode_summary")
        if isinstance(rows, list):
            return [row for row in rows if isinstance(row, dict)]
    rows = report.get("mode_summary")
    if isinstance(rows, list):
        return [row for row in rows if isinstance(row, dict)]
    return []


def find_mode_summary(
    rows: list[dict[str, Any]],
    *,
    backend: str,
    mode: str,
) -> dict[str, Any] | None:
    for row in rows:
        if str(row.get("backend")) == backend and str(row.get("mode")) == mode:
            return row
    return None


def build_spectre_ax_gate(
    same_server: dict[str, Any],
    *,
    evas_mode: str,
    spectre_ax_mode: str,
    require_artifact_claim_allowed: bool,
) -> dict[str, Any]:
    blockers: list[str] = []
    if not same_server:
        return {
            "claim": "evas_faster_than_spectre_ax",
            "allowed": False,
            "scope": "same-slice same-server EVAS/Spectre AX timing",
            "evas_mode": evas_mode,
            "spectre_ax_mode": spectre_ax_mode,
            "blockers": ["missing_same_server_ax_artifact"],
        }

    if require_artifact_claim_allowed and not bool_true(same_server.get("claim_allowed")):
        blockers.append("same_server_artifact_claim_allowed_false")

    rows = mode_summary_rows(same_server)
    evas = find_mode_summary(rows, backend="evas", mode=evas_mode)
    ax = find_mode_summary(rows, backend="spectre", mode=spectre_ax_mode)
    if evas is None:
        blockers.append("missing_evas_mode_summary")
    if ax is None:
        blockers.append("missing_spectre_ax_mode_summary")

    evas_wall = float_or_none(evas.get("total_wall_time_s")) if evas else None
    ax_wall = float_or_none(ax.get("total_wall_time_s")) if ax else None
    speedup = ax_wall / evas_wall if evas_wall and ax_wall and evas_wall > 0.0 else None
    if speedup is None:
        blockers.append("missing_comparable_total_wall")
    elif speedup <= 1.0:
        blockers.append("evas_not_faster_than_spectre_ax")

    parity = same_server.get("parity_safety", {})
    if isinstance(parity, dict):
        violations = parity.get("violations", [])
        if violations:
            blockers.append("parity_safety_violations_present")
    else:
        blockers.append("missing_parity_safety")

    return {
        "claim": "evas_faster_than_spectre_ax",
        "allowed": not blockers,
        "scope": "same-slice same-server EVAS/Spectre AX timing",
        "evas_mode": evas_mode,
        "spectre_ax_mode": spectre_ax_mode,
        "require_artifact_claim_allowed": require_artifact_claim_allowed,
        "same_server_claim_allowed": bool_true(same_server.get("claim_allowed")),
        "evas_total_wall_s": evas_wall,
        "spectre_ax_total_wall_s": ax_wall,
        "spectre_ax_over_evas_speedup": speedup,
        "blockers": blockers,
    }


def build_report(
    *,
    coverage_json: Path | None = DEFAULT_COVERAGE_JSON,
    stage_json: Path | None = DEFAULT_STAGE_JSON,
    same_server_json: Path | None = None,
    min_stage_completion: float = DEFAULT_MIN_STAGE_COMPLETION,
    full_rust_percent: float = DEFAULT_FULL_RUST_PERCENT,
    evas_mode: str = "profile_fast_rust_55",
    spectre_ax_mode: str = "ax_speed",
    require_artifact_claim_allowed: bool = True,
) -> dict[str, Any]:
    coverage = read_json(coverage_json)
    stage = read_json(stage_json)
    same_server = read_json(same_server_json)

    gates = {
        "stage55_topwall_engineering_speedup": build_stage_gate(
            stage,
            min_completion=min_stage_completion,
        ),
        "full_release_rustification": build_full_rust_gate(
            coverage,
            full_rust_percent=full_rust_percent,
        ),
        "evas_faster_than_spectre_ax": build_spectre_ax_gate(
            same_server,
            evas_mode=evas_mode,
            spectre_ax_mode=spectre_ax_mode,
            require_artifact_claim_allowed=require_artifact_claim_allowed,
        ),
    }
    return {
        "schema_version": SCHEMA_VERSION,
        "artifact_kind": "evas_rust_speed_claim_gate",
        "date": date.today().isoformat(),
        "claim_policy": {
            "paper_speed_claim_allowed": gates["evas_faster_than_spectre_ax"]["allowed"],
            "full_rustification_claim_allowed": gates["full_release_rustification"]["allowed"],
            "engineering_stage_claim_allowed": gates["stage55_topwall_engineering_speedup"]["allowed"],
        },
        "inputs": {
            "coverage_json": rel(coverage_json) if coverage_json else None,
            "stage_json": rel(stage_json) if stage_json else None,
            "same_server_json": rel(same_server_json) if same_server_json else None,
        },
        "gates": gates,
    }


def write_markdown(report: dict[str, Any], path: Path) -> None:
    gates = report["gates"]
    lines = [
        "# Rust Speed Claim Gate",
        "",
        f"Date: `{report['date']}`",
        "",
        "## Verdict",
        "",
        "| Claim | Allowed | Reason |",
        "|---|---:|---|",
    ]
    for key, gate in gates.items():
        blockers = gate.get("blockers", [])
        reason = "pass" if not blockers else ", ".join(f"`{item}`" for item in blockers)
        lines.append(f"| `{key}` | `{gate['allowed']}` | {reason} |")

    stage = gates["stage55_topwall_engineering_speedup"]
    full = gates["full_release_rustification"]
    ax = gates["evas_faster_than_spectre_ax"]
    lines.extend(
        [
            "",
            "## Stage 55 Engineering Gate",
            "",
            f"- Observed completion: `{stage['observed_completion_percent']}%`",
            f"- Total wall speedup: `{stage['total_wall_speedup']}`",
            f"- Scope: {stage['scope']}",
            "",
            "## Full Rustification Gate",
            "",
            f"- Observed release Rustification estimate: `{full['observed_percent']}%`",
            f"- Threshold for full Rustification claim: `{full['threshold_percent']}%`",
            f"- Behavior blocker count: `{full['behavior_blocker_count']}`",
            "",
            "## Spectre AX Speed Gate",
            "",
            f"- EVAS mode: `{ax['evas_mode']}`",
            f"- Spectre AX mode: `{ax['spectre_ax_mode']}`",
            f"- EVAS total wall: `{ax.get('evas_total_wall_s')}`",
            f"- Spectre AX total wall: `{ax.get('spectre_ax_total_wall_s')}`",
            f"- AX/EVAS speedup: `{ax.get('spectre_ax_over_evas_speedup')}`",
            "",
            "## Next Required Work",
            "",
            "- To claim full Rustification: remove all production behavior blockers in the release coverage manifest, not just top-wall fastpaths.",
            "- To claim faster than Spectre AX: run `profile_fast_rust_55` and Spectre AX on the same slice, same server, same settings, with repeated cold/warm runs and equivalence gates.",
        ]
    )
    if full["behavior_blockers"]:
        lines.extend(["", "## Top Full-Rustification Blockers", "", "| ID | Status | Present rows |", "|---|---|---:|"])
        for row in full["behavior_blockers"]:
            lines.append(
                f"| `{row['id']}` | `{row['status']}` | {row['present_model_rows']} |"
            )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build EVAS Rust speed claim gate.")
    parser.add_argument("--coverage-json", default=str(DEFAULT_COVERAGE_JSON))
    parser.add_argument("--stage-json", default=str(DEFAULT_STAGE_JSON))
    parser.add_argument("--same-server-json", default=None)
    parser.add_argument("--evas-mode", default="profile_fast_rust_55")
    parser.add_argument("--spectre-ax-mode", default="ax_speed")
    parser.add_argument("--min-stage-completion", type=float, default=DEFAULT_MIN_STAGE_COMPLETION)
    parser.add_argument("--full-rust-percent", type=float, default=DEFAULT_FULL_RUST_PERCENT)
    parser.add_argument(
        "--allow-diagnostic-same-server",
        action="store_true",
        help="Do not require the same-server artifact's own claim_allowed field to be true.",
    )
    parser.add_argument("--report-json", default=str(DEFAULT_REPORT_JSON))
    parser.add_argument("--report-md", default=str(DEFAULT_REPORT_MD))
    return parser.parse_args()


def resolve_optional_path(value: str | None) -> Path | None:
    if value is None:
        return None
    path = Path(value)
    if not path.is_absolute():
        path = ROOT / path
    return path


def main() -> None:
    args = parse_args()
    report_json = resolve_optional_path(args.report_json)
    report_md = resolve_optional_path(args.report_md)
    assert report_json is not None
    assert report_md is not None
    report = build_report(
        coverage_json=resolve_optional_path(args.coverage_json),
        stage_json=resolve_optional_path(args.stage_json),
        same_server_json=resolve_optional_path(args.same_server_json),
        min_stage_completion=args.min_stage_completion,
        full_rust_percent=args.full_rust_percent,
        evas_mode=args.evas_mode,
        spectre_ax_mode=args.spectre_ax_mode,
        require_artifact_claim_allowed=not args.allow_diagnostic_same_server,
    )
    report_json.parent.mkdir(parents=True, exist_ok=True)
    report_json.write_text(json.dumps(report, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    write_markdown(report, report_md)
    print(
        "wrote rust speed claim gate: stage={stage} full_rust={full} ax_speed={ax} report={report}".format(
            stage=report["gates"]["stage55_topwall_engineering_speedup"]["allowed"],
            full=report["gates"]["full_release_rustification"]["allowed"],
            ax=report["gates"]["evas_faster_than_spectre_ax"]["allowed"],
            report=rel(report_json),
        )
    )


if __name__ == "__main__":
    main()
