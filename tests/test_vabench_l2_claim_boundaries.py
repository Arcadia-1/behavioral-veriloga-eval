from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "benchmark-vabench-release-v1"
MANIFEST = PACKAGE / "MANIFEST.json"


def _manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def _l2_forms() -> list[dict]:
    return [row for row in _manifest()["forms"] if row["level"] == "L2"]


def _l2_entries() -> list[dict]:
    return [row for row in _manifest()["entries"] if row["level"] == "L2"]


def test_l2_prompts_declare_background_and_claim_boundary() -> None:
    forms = _l2_forms()

    assert len(forms) == 55
    for row in forms:
        prompt = ROOT / row["prompt"]
        text = prompt.read_text(encoding="utf-8")

        assert "## L2 Background And Claim Boundary" in text, row["id"]
        assert "intermediate state" in text or "support flow" in text, row["id"]
        assert "Paper-facing claims" in text, row["id"]
        assert "Hidden evaluator boundary" in text, row["id"]


def test_support_l2_rows_are_not_core_score_rows() -> None:
    support_entries = [row for row in _l2_entries() if row["track"] == "support"]

    assert len(support_entries) == 3
    assert all(row["counted_in_score"] is False for row in support_entries)
    assert all(row["content_denominator_included"] is False for row in support_entries)


def test_l2_local_metadata_does_not_contradict_release_certification() -> None:
    stale_tokens = [
        "pending_until_evas_spectre_rerun",
        "pending_dual",
        "fresh_dual_pending",
        "fresh-dual",
        "behavior-mismatch",
        '"verification_status": "failed"',
        '"verification_status": "pending"',
    ]

    for row in _l2_forms():
        for key in ("meta", "checks"):
            path = ROOT / row[key]
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            assert not any(token in lowered for token in stale_tokens), f"{row['id']} {key}"

    for entry in _l2_entries():
        path = ROOT / entry["release_entry_manifest"]
        text = path.read_text(encoding="utf-8").lower()
        assert "source_pending_dual" not in text, entry["release_entry_id"]
