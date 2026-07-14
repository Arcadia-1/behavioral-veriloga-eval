from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


def load_script(name: str):
    for directory in (ROOT / "scripts", ROOT / "runners"):
        if str(directory) not in sys.path:
            sys.path.insert(0, str(directory))
    script = ROOT / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, script)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_engine_env_selects_expected_repo_and_backend(tmp_path: Path) -> None:
    compare = load_script("run_v3_evas_engine_compare")
    main_repo = tmp_path / "main"
    skeleton_repo = tmp_path / "skeleton"

    assert compare.engine_env("python", main_repo, skeleton_repo) == {
        "VAEVAS_EVAS_REPO": str(main_repo),
        "VAEVAS_DEFAULT_EVAS_ENGINE": "python",
        "EVAS_ENGINE": "python",
    }
    assert compare.engine_env("python_rust", main_repo, skeleton_repo) == {
        "VAEVAS_EVAS_REPO": str(main_repo),
        "VAEVAS_DEFAULT_EVAS_ENGINE": "evas2",
        "EVAS_ENGINE": "evas2",
    }
    assert compare.engine_env("pure_rust_skeleton", main_repo, skeleton_repo) == {
        "VAEVAS_EVAS_REPO": str(skeleton_repo),
        "VAEVAS_DEFAULT_EVAS_ENGINE": "evas2",
        "EVAS_ENGINE": "evas2",
    }


def test_engine_env_rejects_unknown_lane(tmp_path: Path) -> None:
    compare = load_script("run_v3_evas_engine_compare")

    with pytest.raises(SystemExit, match="unknown engine label"):
        compare.engine_env("unknown", tmp_path / "main", tmp_path / "skeleton")


def test_version_policy_rejects_mixed_or_stale_evas_repos() -> None:
    parity = load_script("run_v3_skeleton_dual_parity")
    report = {
        "same_kernel_head": False,
        "main_evas_repo": {
            "describe": "main-head",
            "contains_upstream_main": True,
        },
        "skeleton_repo": {
            "describe": "skeleton-head",
            "contains_upstream_main": False,
        },
    }

    with pytest.raises(SystemExit, match="different HEADs") as error:
        parity.enforce_evas_version_policy(
            report,
            argparse.Namespace(allow_mixed_evas_repos=False),
        )

    assert "does not contain local upstream/main" in str(error.value)


def test_version_policy_allows_explicit_comparison_run() -> None:
    parity = load_script("run_v3_skeleton_dual_parity")
    report = {
        "same_kernel_head": False,
        "main_evas_repo": {"describe": "main-head", "contains_upstream_main": True},
        "skeleton_repo": {"describe": "skeleton-head", "contains_upstream_main": False},
    }

    parity.enforce_evas_version_policy(
        report,
        argparse.Namespace(allow_mixed_evas_repos=True),
    )


def test_spectre_cache_requires_current_matching_testbench(tmp_path: Path) -> None:
    parity = load_script("run_v3_skeleton_dual_parity")
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()
    testbench = tmp_path / "hidden.scs"

    matches, reason = parity.spectre_cache_matches_case(cache_dir, {"tb": testbench})
    assert not matches
    assert reason == "current testbench missing"

    testbench.write_text("simulator lang=spectre\ntran tran stop=1n\n", encoding="utf-8")
    cached = cache_dir / "materialized.scs"
    cached.write_text("simulator lang=spectre\ntran tran stop=2n\n", encoding="utf-8")
    matches, reason = parity.spectre_cache_matches_case(cache_dir, {"tb": testbench})
    assert not matches
    assert reason == "cached spectre netlist does not match current testbench"

    cached.write_text("\n" + testbench.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    matches, reason = parity.spectre_cache_matches_case(cache_dir, {"tb": testbench})
    assert matches
    assert reason == "matched materialized.scs"
