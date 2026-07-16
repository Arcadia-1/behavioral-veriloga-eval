#!/usr/bin/env python3
"""Run the batch-34 affine timing metamorphic suite through EVAS.

The transformed testbench uses ``t' = 1.37*t + 2 ns``.  Only time-bearing
source tokens are changed; voltage values and DUT sources remain untouched.
The output is a compact evidence record, not simulator/raw trace data.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path
from typing import Any


A = 1.37
B = 2e-9
TIME_RE = re.compile(
    r"^(?P<num>[+-]?(?:\d+(?:\.\d*)?|\.\d+))(?P<unit>[munpf])?$"
)
KV_RE = re.compile(
    r"(?P<key>stop|maxstep|period|width|delay|rise|fall)="
    r"(?P<value>[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[munpf])?)"
)
UNIT_SCALE = {"m": 1e-3, "u": 1e-6, "n": 1e-9, "p": 1e-12, "f": 1e-15}


def _parse_time(token: str) -> float | None:
    match = TIME_RE.fullmatch(token)
    if match is None:
        return None
    return float(match.group("num")) * UNIT_SCALE.get(match.group("unit"), 1.0)


def _format_time(seconds: float) -> str:
    if abs(seconds) >= 1e-9:
        return f"{seconds / 1e-9:.12g}n"
    return f"{seconds / 1e-12:.12g}p"


def _transform_wave(match: re.Match[str], *, scale: float, offset: float) -> str:
    content = match.group(1)
    pieces = re.split(r"(\s+|\\)", content)
    ordinal = 0
    transformed: list[str] = []
    for piece in pieces:
        if not piece or piece.isspace() or piece == "\\":
            transformed.append(piece)
            continue
        if ordinal % 2 == 0:
            parsed = _parse_time(piece)
            transformed.append(
                _format_time(scale * parsed + offset) if parsed is not None else piece
            )
        else:
            transformed.append(piece)
        ordinal += 1
    return "wave=[" + "".join(transformed) + "]"


def transform_deck(text: str, *, scale: float = A, offset: float = B) -> str:
    """Apply an affine time transform while preserving voltage literals."""
    def transform_wave(match: re.Match[str]) -> str:
        return _transform_wave(match, scale=scale, offset=offset)

    transformed = re.sub(r"wave=\[(.*?)\]", transform_wave, text, flags=re.S)

    def replace_key_value(match: re.Match[str]) -> str:
        key = match.group("key")
        parsed = _parse_time(match.group("value"))
        if parsed is None:
            return match.group(0)
        translated = scale * parsed + (offset if key in {"stop", "delay"} else 0.0)
        return f"{key}={_format_time(translated)}"

    return KV_RE.sub(replace_key_value, transformed)


def _run_family(root: Path, family: int) -> dict[str, Any]:
    sys.path.insert(0, str(root.parents[1] / "runners"))
    from derived_testbench_oracle import _run_case

    task = next(root.glob(f"tasks/{500 + family:03d}-*-testbench"))
    contract = json.loads((task / "public_contract.json").read_text(encoding="utf-8"))
    checker = json.loads((task / "evaluator" / "checker_profile.json").read_text(encoding="utf-8"))
    family_spec = json.loads((task / "evaluator" / "family_spec.json").read_text(encoding="utf-8"))
    artifacts = [str(item["path"]) for item in family_spec["artifact_contract"]["files"]]
    original = (task / "evaluator" / "reference_tb.scs").read_text(encoding="utf-8")
    transformed = transform_deck(original)
    with tempfile.NamedTemporaryFile("w", suffix=".scs", prefix=f"v4_b34_meta_{family}_", delete=False) as handle:
        handle.write(transformed)
        transformed_tb = Path(handle.name)
    common = {
        "package_root": root,
        "tb_source": transformed_tb,
        "source_formal": task / "evaluator",
        "target_artifacts": artifacts,
        "checker_task_id": checker["checker_task_id"],
        "required_signals": set(contract["trace_contract"]["required_signals"]),
        "public_contract": contract,
        "dut_subdir": "dut",
    }
    try:
        reference = _run_case(**common, negative_bundle=None, label=f"v4-{500 + family}-meta-gold")
        negatives = []
        for bundle in sorted((task / "evaluator" / "mutation_bundles").glob("neg_*")):
            result = _run_case(
                **common,
                negative_bundle=bundle,
                label=f"v4-{500 + family}-meta-{bundle.name}",
            )
            negatives.append({"id": bundle.name, "outcome": result.outcome.value})
        return {
            "family": family,
            "reference": reference.outcome.value,
            "negative_outcomes": negatives,
            "transformed_deck_sha256": hashlib.sha256(transformed.encode()).hexdigest(),
        }
    finally:
        transformed_tb.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--release", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-workers", type=int, default=4)
    args = parser.parse_args()
    families = range(331, 341)
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.max_workers) as pool:
        results = list(pool.map(lambda family: _run_family(args.release.resolve(), family), families))
    results.sort(key=lambda item: int(item["family"]))
    payload = {
        "schema_version": "v4-batch34-metamorphic-evas-v1",
        "transform": {"scale": A, "offset_seconds": B, "formula": "t'=1.37*t+2ns"},
        "family_count": len(results),
        "reference_pass_count": sum(item["reference"] == "reference_pass" for item in results),
        "negative_kill_count": sum(
            negative["outcome"] == "killed_behaviorally"
            for item in results
            for negative in item["negative_outcomes"]
        ),
        "negative_count": sum(len(item["negative_outcomes"]) for item in results),
        "families": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: payload[key] for key in ("family_count", "reference_pass_count", "negative_kill_count", "negative_count")}, sort_keys=True))
    return 0 if payload["reference_pass_count"] == 10 and payload["negative_kill_count"] == payload["negative_count"] == 50 else 1


if __name__ == "__main__":
    raise SystemExit(main())
