#!/usr/bin/env python3
"""Apply the frozen generic direct-response normalizer to stored pilot outputs."""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("v4_calibration_runner", HERE / "run_campaign.py")
assert SPEC and SPEC.loader
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def refresh_summary(root: Path) -> None:
    results = [
        read_json(path)
        for path in sorted(root.glob("v4-*/evidence/campaign_result.json"))
    ]
    summary_path = root / "SUMMARY.json"
    summary = read_json(summary_path) if summary_path.is_file() else {
        "schema_version": "v4-calibration-run-summary-v1"
    }
    summary["result_count"] = len(results)
    summary["statuses"] = dict(sorted(Counter(row["status"] for row in results).items()))
    summary["deterministic_direct_normalization_count"] = sum(
        bool(row.get("normalization_record")) for row in results
    )
    write_json(summary_path, summary)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--campaign-output", type=Path, required=True)
    args = parser.parse_args()
    changed = []
    for result_path in sorted(args.campaign_output.glob("v4-*/evidence/campaign_result.json")):
        result = read_json(result_path)
        if result.get("status") != "invalid_submission" or result.get("cell", {}).get("process") != "direct_one_shot":
            continue
        runtime = result_path.parents[1]
        checkpoint = read_json(runtime / "evidence" / "conversation_checkpoint.json")
        content = str(checkpoint["messages"][-1].get("content") or "")
        saved, protocol = RUNNER.extract_direct_with_protocol(content, runtime)
        if not saved or not RUNNER.submission_complete(runtime):
            continue
        result.update({
            "status": "submitted",
            "saved_files": saved,
            "extraction_protocol": protocol,
            "submission_protocol_compliant": RUNNER.direct_protocol_compliant(protocol),
            "normalized_from_status": "invalid_submission",
            "normalized_at": datetime.now(timezone.utc).isoformat(),
            "normalization_record": {
                "kind": "deterministic_direct_response_extraction",
                "model_invoked": False,
                "response_sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
                "artifact_sha256": {
                    relative: hashlib.sha256(
                        (runtime / "public" / "submission" / relative).read_bytes()
                    ).hexdigest()
                    for relative in saved
                },
            },
        })
        write_json(result_path, result)
        changed.append(result["cell"]["cell_id"])
    refresh_summary(args.campaign_output)
    print(json.dumps({"normalized_count": len(changed), "cell_ids": changed}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
