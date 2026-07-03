from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "run_v3_evas_lint_preflight.py"


def load_lint_module():
    runners = str(ROOT / "runners")
    if runners not in sys.path:
        sys.path.insert(0, runners)
    spec = importlib.util.spec_from_file_location("run_v3_evas_lint_preflight", SCRIPT)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def make_dut_task(root: Path) -> Path:
    task = root / "001-demo-dut"
    (task / "solution").mkdir(parents=True)
    (task / "test_hidden" / "tests").mkdir(parents=True)
    (task / "task.toml").write_text(
        'id = "demo_dut"\ntarget = ["demo.va"]\n',
        encoding="utf-8",
    )
    (task / "solution" / "demo.va").write_text(
        "`include \"disciplines.vams\"\nmodule demo(input a, output y); electrical a, y; analog V(y) <+ V(a); endmodule\n",
        encoding="utf-8",
    )
    (task / "test_hidden" / "tests" / "tb_demo.scs").write_text(
        'simulator lang=spectre\nahdl_include "demo.va"\ntran tran stop=1n\n',
        encoding="utf-8",
    )
    return task


def make_tb_task(root: Path) -> Path:
    task = root / "002-demo-testbench"
    (task / "solution").mkdir(parents=True)
    (task / "task.toml").write_text(
        'id = "demo_tb"\ntarget = ["tb_demo.scs"]\n',
        encoding="utf-8",
    )
    (task / "solution" / "demo.va").write_text(
        "`include \"disciplines.vams\"\nmodule demo(output y); electrical y; analog V(y) <+ 0.0; endmodule\n",
        encoding="utf-8",
    )
    (task / "solution" / "tb_demo.scs").write_text(
        'simulator lang=spectre\nahdl_include "demo.va"\ntran tran stop=1n\n',
        encoding="utf-8",
    )
    return task


def test_collects_hidden_dut_case_and_stages_candidate_source(tmp_path: Path) -> None:
    lint = load_lint_module()
    task = make_dut_task(tmp_path)

    cases, notes = lint.collect_lint_cases(task, artifact_root_name="solution", split="hidden")

    assert notes == []
    assert [case.case_id for case in cases] == ["001-demo-dut:hidden:tb_demo.scs"]
    staged_root = tmp_path / "stage"
    staged_root.mkdir()
    staged_input = lint.stage_lint_case(cases[0], staged_root)
    assert staged_input.name == "tb_demo.scs"
    assert (staged_root / "demo.va").exists()


def test_collects_target_scs_for_testbench_tasks(tmp_path: Path) -> None:
    lint = load_lint_module()
    task = make_tb_task(tmp_path)

    cases, notes = lint.collect_lint_cases(task, artifact_root_name="solution", split="hidden")

    assert notes == []
    assert [case.case_id for case in cases] == ["002-demo-testbench:target:tb_demo.scs"]
    staged_root = tmp_path / "stage"
    staged_root.mkdir()
    staged_input = lint.stage_lint_case(cases[0], staged_root)
    assert staged_input.name == "tb_demo.scs"
    assert (staged_root / "demo.va").exists()


def test_lint_summary_counts_warnings_and_compat_errors(tmp_path: Path) -> None:
    lint = load_lint_module()
    task = make_dut_task(tmp_path)
    cases, _notes = lint.collect_lint_cases(task, artifact_root_name="solution", split="hidden")

    def fake_runner(_input_path: Path, _min_transition: float, _timeout_s: int):
        return (
            1,
            [
                {
                    "code": "EVAS-AHDL-W5003",
                    "severity": "static-warning",
                    "file": str(_input_path.parent / "demo.va"),
                },
                {"code": "EVAS-COMP-EINCLUDE", "severity": "compat-error", "file": str(_input_path)},
            ],
            "[]",
        )

    row = lint.lint_one_case(
        cases[0],
        min_transition=1e-12,
        timeout_s=1,
        max_diagnostics=20,
        runner=fake_runner,
    )
    payload = lint.build_payload([row], [], split="hidden")

    assert row["status"] == "FAIL_COMPAT"
    assert row["diagnostics"][0]["file"] == "demo.va"
    assert row["diagnostics"][1]["file"] == "tb_demo.scs"
    assert payload["summary"]["compat_error_count"] == 1
    assert payload["summary"]["warning_count"] == 1


def test_run_evas_lint_falls_back_to_sibling_venv_executable(tmp_path: Path, monkeypatch) -> None:
    lint = load_lint_module()
    bin_dir = tmp_path / "venv" / "bin"
    bin_dir.mkdir(parents=True)
    python_path = bin_dir / "python"
    evas_path = bin_dir / "evas"
    python_path.write_text("", encoding="utf-8")
    evas_path.write_text("", encoding="utf-8")
    input_path = tmp_path / "tb.scs"
    input_path.write_text("simulator lang=spectre\n", encoding="utf-8")

    captured: dict[str, object] = {}

    def fake_run(cmd, **kwargs):
        captured["cmd"] = cmd
        captured["cwd"] = kwargs["cwd"]

        class Result:
            returncode = 0
            stdout = "[]"
            stderr = ""

        return Result()

    monkeypatch.setattr(lint, "evas_command_and_env", lambda: (["evas"], None))
    monkeypatch.setattr(lint.sys, "executable", str(python_path))
    monkeypatch.setattr(lint.subprocess, "run", fake_run)

    returncode, diagnostics, raw_output = lint.run_evas_lint(input_path, 1e-12, 5)

    assert returncode == 0
    assert diagnostics == []
    assert raw_output == "[]"
    assert captured["cmd"][0] == str(evas_path)
    assert captured["cwd"] == input_path.parent
