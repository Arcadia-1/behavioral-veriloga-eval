from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runners"))

from export_vabench_github_pages import export_site  # noqa: E402


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_github_pages_export_materializes_current_300_surface(tmp_path: Path) -> None:
    written = export_site(tmp_path)

    assert set(written) == {
        "backend_coverage.json",
        "category_coverage.json",
        "site_summary.json",
        "task_gallery.json",
    }

    site = read_json(tmp_path / "site_summary.json")
    backends = read_json(tmp_path / "backend_coverage.json")
    tasks = read_json(tmp_path / "task_gallery.json")
    categories = read_json(tmp_path / "category_coverage.json")

    assert site["summary"]["form_count"] == 300
    assert site["summary"]["entry_count"] == 86
    assert site["summary"]["four_backend_status"] == "pass"
    assert site["provenance"]["public_denominator"] == 300
    assert site["provenance"]["inherited_v1_rows"] == 271
    assert site["provenance"]["promoted_v1_1_rows"] == 29

    assert backends["status"] == "pass"
    assert len(backends["rows"]) == 4
    assert all(row["certification_passed"] for row in backends["rows"])
    assert all(row["pass_rows"] == 300 for row in backends["rows"])
    assert all(row["total_rows"] == 300 for row in backends["rows"])

    assert tasks["summary"]["row_count"] == 300
    assert tasks["summary"]["promoted_v1_1_rows"] == 29
    assert tasks["summary"]["inherited_v1_rows"] == 271
    assert tasks["summary"]["certified_rows"] == 300
    assert len(tasks["rows"]) == 300
    assert "Data Converter Models" in tasks["filters"]["category"]

    assert len(categories["rows"]) == 10


def test_model_eval_guide_is_linked_to_current_roster() -> None:
    index = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    guide = (ROOT / "docs" / "run-model-eval.html").read_text(encoding="utf-8")
    accuracy = (ROOT / "docs" / "accuracy.html").read_text(encoding="utf-8")
    site_script = (ROOT / "docs" / "assets" / "site.js").read_text(encoding="utf-8")
    script = (ROOT / "docs" / "assets" / "run-model-eval.js").read_text(encoding="utf-8")
    roster = read_json(ROOT / "docs" / "data" / "model_eval_roster.json")

    for page in [
        "leaderboard.html",
        "benchmark.html",
        "run-model-eval.html",
        "protocol.html",
        "accuracy.html",
        "news.html",
        "contributors.html",
    ]:
        assert f'href="{page}"' in index
        assert (ROOT / "docs" / page).exists()

    assert 'href="run-model-eval.html"' in index
    assert 'assets/run-model-eval.js' in guide
    assert 'assets/site.js' in index
    assert 'data/site_summary.json' in site_script
    assert 'data/precision_overview.json' in site_script
    assert 'data/model_eval_roster.json' in script
    assert "DeepSeek V4 Flash smoke" in guide
    assert "OpenAI-compatible" in guide
    assert "Spectre final judge" in guide
    assert "navAccuracy" in script
    assert "NEWS_ITEMS" in site_script
    assert "VERIFIED_LEADERBOARD_ROWS" in site_script
    assert "pointwise-taxonomy" in accuracy
    assert "task-metric-table" in accuracy
    assert "renderPointwiseTaxonomy" in site_script
    assert "renderTaskMetricRows" in site_script
    assert roster["summary"]["scored_model_row_count"] == 265
    assert "deepseek_v4_flash_smoke" in roster["example_commands"]
    assert "full_eval_with_spectre" in roster["example_commands"]


def test_docs_are_publishable_by_github_pages_actions() -> None:
    workflow = (ROOT / ".github" / "workflows" / "pages.yml").read_text(encoding="utf-8")

    assert (ROOT / "docs" / ".nojekyll").exists()
    assert "actions/configure-pages" in workflow
    assert "actions/upload-pages-artifact" in workflow
    assert "actions/deploy-pages" in workflow
    assert "path: docs" in workflow
    assert "workflow_dispatch" in workflow
