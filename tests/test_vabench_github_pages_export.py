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
        "task_details.json",
        "task_gallery.json",
    }

    site = read_json(tmp_path / "site_summary.json")
    backends = read_json(tmp_path / "backend_coverage.json")
    tasks = read_json(tmp_path / "task_gallery.json")
    task_details = read_json(tmp_path / "task_details.json")
    categories = read_json(tmp_path / "category_coverage.json")

    assert site["summary"]["form_count"] == 300
    assert site["summary"]["entry_count"] == 86
    assert site["summary"]["four_backend_status"] == "pass"
    assert site["summary"]["paper_score_ready_task_count"] == 300
    assert site["provenance"]["public_denominator"] == 300
    assert site["provenance"]["inherited_v1_rows"] == 271
    assert site["provenance"]["promoted_v1_1_rows"] == 29
    assert site["provenance"]["provisional_v1_1_rows"] == 0

    assert backends["status"] == "pass"
    assert len(backends["rows"]) == 4
    assert all(row["certification_passed"] for row in backends["rows"])
    assert all(row["pass_rows"] == 300 for row in backends["rows"])
    assert all(row["total_rows"] == 300 for row in backends["rows"])

    assert tasks["summary"]["row_count"] == 300
    assert tasks["summary"]["promoted_v1_1_rows"] == 29
    assert tasks["summary"]["provisional_v1_1_rows"] == 0
    assert tasks["summary"]["inherited_v1_rows"] == 271
    assert tasks["summary"]["certified_rows"] == 300
    assert len(tasks["rows"]) == 300
    assert "Data Converter Models" in tasks["filters"]["category"]
    assert sum(1 for row in tasks["rows"] if row.get("prompt")) == 300
    assert sum(1 for row in tasks["rows"] if row.get("prompt") is None) == 0
    assert sum(1 for row in tasks["rows"] if row.get("checks")) == 300
    assert sum(1 for row in tasks["rows"] if row.get("release_task_manifest")) == 300
    assert sum(1 for row in tasks["rows"] if row["provenance"] == "promoted_v1.1" and row.get("prompt")) == 29
    prompt_row = next(row for row in tasks["rows"] if row.get("prompt"))
    assert prompt_row["checks"].endswith("checks.yaml")
    assert prompt_row["release_task_manifest"].endswith("release_task.json")
    assert isinstance(prompt_row["gold_count"], int)

    assert task_details["summary"]["row_count"] == 300
    assert task_details["summary"]["prompt_count"] == 300
    assert task_details["summary"]["checks_count"] == 300
    assert task_details["summary"]["meta_count"] == 300
    assert task_details["summary"]["release_task_count"] == 300
    assert task_details["summary"]["gold_file_count"] >= 600
    assert task_details["summary"]["truncated_file_count"] == 0
    detail_row = next(
        row
        for row in task_details["rows"]
        if row["release_entry_id"] == prompt_row["release_entry_id"] and row["form"] == prompt_row["form"]
    )
    detail_files = {file["kind"]: file for file in detail_row["files"] if file["kind"] != "gold"}
    assert detail_files["prompt"]["content"]
    assert detail_files["checks"]["content"]
    assert detail_files["release_task"]["content"]
    assert any(file["kind"] == "gold" and file["content"] for file in detail_row["files"])

    assert len(categories["rows"]) == 10


def test_model_eval_guide_is_linked_to_current_roster() -> None:
    index = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    guide = (ROOT / "docs" / "run-model-eval.html").read_text(encoding="utf-8")
    accuracy = (ROOT / "docs" / "accuracy.html").read_text(encoding="utf-8")
    benchmark = (ROOT / "docs" / "benchmark.html").read_text(encoding="utf-8")
    task_detail = (ROOT / "docs" / "task.html").read_text(encoding="utf-8")
    accuracy_case = (ROOT / "docs" / "accuracy-case.html").read_text(encoding="utf-8")
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
    assert 'data/task_details.json' in site_script
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
    assert "id-guide" in benchmark
    assert "idGuideVbr1" in benchmark
    assert "idGuideVbr11" in benchmark
    assert 'data-page="task-detail"' in task_detail
    assert "task-detail-identity" in task_detail
    assert "task-detail-content-list" in task_detail
    assert "task-detail-accuracy-table" in task_detail
    assert 'data-page="accuracy-case"' in accuracy_case
    assert "accuracy-case-taxonomy" in accuracy_case
    assert "task.html?" in site_script
    assert "accuracy-case.html?" in site_script
    assert "renderTaskDetail" in site_script
    assert "renderTaskDetailContents" in site_script
    assert "idNamespaceMeaning" in site_script
    assert "labelIdNamespace" in site_script
    assert "renderAccuracyCase" in site_script
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
