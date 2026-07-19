from __future__ import annotations

import io
import json
import shutil
import sys
import tarfile
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runners"))

import run_gold_dual_suite as dual  # noqa: E402
import run_gold_suite as gold_suite  # noqa: E402


def test_write_spectre_psf_csv_ignores_saved_time_trace_collision(tmp_path: Path) -> None:
    raw_dir = tmp_path / "score_tb.raw"
    raw_dir.mkdir()
    (raw_dir / "tran.tran.tran").write_text(
        """HEADER
TYPE
SWEEP
"time" "sweep" PROP(
"sweep_direction" 0
"units" "s"
"plot" 1
"grid" 1
)
TRACE
"time" "param_real"
"out" "V"
VALUE
"time" 0
"time" 0
"out" 0.25
"time" 1e-9
"time" 0
"out" 0.75
"time" 2e-9
"time" 0
"out" 1.25
""",
        encoding="utf-8",
    )
    csv_path = tmp_path / "tran_spectre.csv"

    result = dual.write_spectre_psf_csv(raw_dir, csv_path)

    assert dual.load_csv_rows(csv_path) == [
        {"time": 0.0, "out": 0.25},
        {"time": 1e-9, "out": 0.75},
        {"time": 2e-9, "out": 1.25},
    ]
    assert result["rows"] == 3
    assert result["duplicate_time_values_ignored"] == 3


def test_write_spectre_psf_csv_preserves_ordinary_time_boundaries(tmp_path: Path) -> None:
    raw_dir = tmp_path / "score_tb.raw"
    raw_dir.mkdir()
    (raw_dir / "tran.tran.tran").write_text(
        """HEADER
TYPE
SWEEP
"time" "sweep" PROP(
"sweep_direction" 0
"units" "s"
"plot" 1
"grid" 1
)
TRACE
"out" "V"
"aux" "V"
VALUE
"time" 0
"out" 0.25
"aux" 10.25
"time" 1e-9
"out" 0.75
"aux" 10.75
"time" 2e-9
"out" 1.25
"aux" 11.25
""",
        encoding="utf-8",
    )
    csv_path = tmp_path / "tran_spectre.csv"

    result = dual.write_spectre_psf_csv(raw_dir, csv_path)

    assert dual.load_csv_rows(csv_path) == [
        {"time": 0.0, "out": 0.25, "aux": 10.25},
        {"time": 1e-9, "out": 0.75, "aux": 10.75},
        {"time": 2e-9, "out": 1.25, "aux": 11.25},
    ]
    assert result["rows"] == 3
    assert result["duplicate_time_values_ignored"] == 0


def test_direct_sui_ssh_base_cmd_disables_stale_controlmaster(monkeypatch) -> None:
    monkeypatch.setenv("VAEVAS_SUI_PROXY_JUMP", "thu-sui")

    cmd = dual.ssh_base_cmd("thu-wei", timeout_s=45)

    assert cmd[:2] == ["ssh", "-o"]
    assert "ControlMaster=no" in cmd
    assert "ControlPath=none" in cmd
    assert cmd[cmd.index("-J") + 1] == "thu-sui"
    assert cmd[-1] == "thu-wei"


def test_run_dual_case_marks_non_scored_behavior_as_not_required(
    monkeypatch, tmp_path: Path
) -> None:
    task_dir = tmp_path / "tasks" / "tb-generation" / "voltage" / "clk_div_min_tb"
    gold_dir = task_dir / "gold"
    gold_dir.mkdir(parents=True)
    tb_path = gold_dir / "tb_clk_div_min_ref.scs"
    dut_path = gold_dir / "clk_div_min.va"
    tb_path.write_text('ahdl_include "clk_div_min.va"\n', encoding="utf-8")
    dut_path.write_text("// stub dut\n", encoding="utf-8")

    monkeypatch.setattr(
        dual,
        "read_meta",
        lambda path: {
            "task_id": "clk_div_min_tb",
            "scoring": ["dut_compile", "tb_compile"],
        },
    )
    monkeypatch.setattr(dual, "choose_gold_tb", lambda gold: tb_path)
    monkeypatch.setattr(dual, "ahdl_includes", lambda tb: [dut_path.name])
    monkeypatch.setattr(gold_suite, "run_gold_case", lambda *args, **kwargs: {"status": "PASS"})
    monkeypatch.setattr(
        dual,
        "run_spectre_case",
        lambda **kwargs: {"status": "success", "ok": True},
    )

    def fail_if_called(*args, **kwargs):
        raise AssertionError("compare_waveforms/evaluate_behavior should not run for non-scored behavior")

    monkeypatch.setattr(dual, "evaluate_behavior", fail_if_called)
    monkeypatch.setattr(dual, "compare_waveforms", fail_if_called)

    result = dual.run_dual_case(
        task_dir=task_dir,
        output_root=tmp_path / "results",
        bridge_repo=tmp_path / "bridge",
        cadence_cshrc=None,
        timeout_s=5,
    )

    assert result["status"] == "PASS"
    assert result["parity"]["status"] == "not_required"
    assert result["spectre"]["behavior_score"] == 1.0
    assert "behavior_not_required_by_scoring" in result["spectre"]["behavior_notes"]
    assert "spectre:behavior_not_required_by_scoring" in result["notes"]


def test_run_spectre_case_passes_bridge_profile(monkeypatch, tmp_path: Path) -> None:
    bridge_repo = tmp_path / "bridge"
    (bridge_repo / ".venv" / "bin").mkdir(parents=True)
    output_dir = tmp_path / "out"
    captured: dict[str, object] = {}

    monkeypatch.setenv("VAEVAS_BRIDGE_PROFILE", "ci")

    def fake_run_cmd(cmd, *, cwd: Path, env=None, timeout_s=None):
        captured["cmd"] = cmd
        captured["cwd"] = cwd
        captured["env"] = env
        captured["timeout_s"] = timeout_s
        captured["inline"] = cmd[-1]
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "spectre_result.json").write_text(
            json.dumps({"status": "success", "ok": True, "errors": [], "warnings": []}),
            encoding="utf-8",
        )
        return SimpleNamespace(stdout="", stderr="", returncode=0)

    monkeypatch.setattr(dual, "run_cmd", fake_run_cmd)
    tb_path = tmp_path / "tb.scs"
    tb_path.write_text("simulator lang=spectre\n", encoding="utf-8")

    result = dual.run_spectre_case(
        task_id="case",
        tb_path=tb_path,
        include_paths=[],
        output_dir=output_dir,
        bridge_repo=bridge_repo,
        cadence_cshrc=None,
        timeout_s=5,
    )

    assert result["ok"] is True
    assert captured["cwd"] == bridge_repo
    assert captured["env"]["VAEVAS_BRIDGE_PROFILE"] == "ci"
    assert '"bridge_profile": "ci"' in captured["inline"]
    assert "profile=profile" in captured["inline"]


def test_run_spectre_case_can_request_side_output_downloads(monkeypatch, tmp_path: Path) -> None:
    bridge_repo = tmp_path / "bridge"
    (bridge_repo / ".venv" / "bin").mkdir(parents=True)
    output_dir = tmp_path / "out"
    captured: dict[str, object] = {}

    def fake_run_cmd(cmd, *, cwd: Path, env=None, timeout_s=None):
        captured["inline"] = cmd[-1]
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "spectre_result.json").write_text(
            json.dumps({"status": "success", "ok": True, "errors": [], "warnings": []}),
            encoding="utf-8",
        )
        return SimpleNamespace(stdout="", stderr="", returncode=0)

    monkeypatch.setattr(dual, "run_cmd", fake_run_cmd)
    tb_path = tmp_path / "tb.scs"
    tb_path.write_text("simulator lang=spectre\n", encoding="utf-8")

    result = dual.run_spectre_case(
        task_id="case",
        tb_path=tb_path,
        include_paths=[],
        output_dir=output_dir,
        bridge_repo=bridge_repo,
        cadence_cshrc=None,
        timeout_s=5,
        side_output_files=("candidate.out",),
    )

    assert result["ok"] is True
    assert '"side_output_files": ["candidate.out"]' in captured["inline"]
    assert "keep_remote_files=bool(side_output_files)" in captured["inline"]
    assert "remote_pwd = next((line for line in reversed(pwd_lines) if line.startswith('/')), '')" in captured["inline"]
    assert "remote_output_dirs.append(candidate_dir)" in captured["inline"]
    assert "runner.download(remote_path, local_path)" in captured["inline"]


def test_gain_extraction_parity_accepts_gain_estimator_output_names() -> None:
    rows = []
    for idx in range(80):
        vin_diff = -0.03 + idx * (0.06 / 79)
        rows.append(
            {
                "time": idx * 1e-9,
                "vinp": 0.45 + 0.5 * vin_diff,
                "vinn": 0.45 - 0.5 * vin_diff,
                "voutp": 0.45 + 3.0 * vin_diff,
                "voutn": 0.45 - 3.0 * vin_diff,
            }
        )

    result = dual.compare_gain_extraction_parity(rows, rows)

    assert result["status"] == "passed"
    assert result["evas"]["output_pair"] == "voutp/voutn"


def test_run_spectre_case_can_use_direct_sui_backend(monkeypatch, tmp_path: Path) -> None:
    output_dir = tmp_path / "out"
    tb_path = tmp_path / "tb.scs"
    va_path = tmp_path / "dut.va"
    tb_path.write_text('simulator lang=spectre\nahdl_include "dut.va"\n', encoding="utf-8")
    va_path.write_text("// stub dut\n", encoding="utf-8")
    psf_text = """HEADER
TYPE
SWEEP
TRACE
"time" "time"
"out" "voltage"
VALUE
"time" 0
"out" 0
"time" 1e-9
"out" 1
"""

    tar_buffer = io.BytesIO()
    with tarfile.open(fileobj=tar_buffer, mode="w:gz") as archive:
        cache_link = tarfile.TarInfo("./case__tb.ahdlSimDB")
        cache_link.type = tarfile.SYMTYPE
        cache_link.linkname = "/tmp/vaevas-direct-spectre/_ahdlcmi_cache/key"
        archive.addfile(cache_link)

        psf_bytes = psf_text.encode("utf-8")
        psf_info = tarfile.TarInfo("case__tb.raw/tran.tran.tran")
        psf_info.size = len(psf_bytes)
        archive.addfile(psf_info, io.BytesIO(psf_bytes))

        log_bytes = b"Number of accepted tran steps = 2\nTime used: elapsed = 1.5 s\n"
        log_info = tarfile.TarInfo("spectre.out")
        log_info.size = len(log_bytes)
        archive.addfile(log_info, io.BytesIO(log_bytes))

        side_bytes = b"side output\n"
        side_info = tarfile.TarInfo("candidate.out")
        side_info.size = len(side_bytes)
        archive.addfile(side_info, io.BytesIO(side_bytes))
    download_tar = tar_buffer.getvalue()
    captured: dict[str, object] = {}
    output_dir.mkdir()
    (output_dir / "case__tb.ahdlSimDB").symlink_to(tmp_path / "stale-cache")

    def fake_run_ssh_text(host, script, *, timeout_s, input_data=None):
        captured.setdefault("text_scripts", []).append(script)
        if "mktemp" in script:
            return SimpleNamespace(stdout="/tmp/vaevas-direct-spectre/case.test\n", stderr="", returncode=0)
        if "AHDLCMI_CACHE_STATUS" in script:
            return SimpleNamespace(
                stdout=(
                    "AHDLCMI_LOCK_DIR=/tmp/vaevas-direct-spectre/_ahdlcmi_cache/key.lock\n"
                    "AHDLCMI_CACHE_STATUS=enabled\n"
                    "AHDLCMI_CACHE_DIR=/tmp/vaevas-direct-spectre/_ahdlcmi_cache/key\n"
                    "AHDLCMI_LINK=/tmp/vaevas-direct-spectre/case.test/case__tb.ahdlSimDB\n"
                ),
                stderr="",
                returncode=0,
            )
        if script.startswith("rmdir "):
            captured.setdefault("unlock_scripts", []).append(script)
            return SimpleNamespace(stdout="", stderr="", returncode=0)
        if "rm -rf" in script:
            captured.setdefault("cleanup_scripts", []).append(script)
            return SimpleNamespace(stdout="", stderr="", returncode=0)
        return SimpleNamespace(stdout="spectre done\n", stderr="", returncode=0)

    def fake_run_ssh_bytes(host, script, *, timeout_s, input_data=None):
        captured.setdefault("byte_scripts", []).append(script)
        if input_data is not None:
            captured["uploaded_bytes"] = len(input_data)
            return SimpleNamespace(stdout=b"", stderr=b"", returncode=0)
        return SimpleNamespace(stdout=download_tar, stderr=b"", returncode=0)

    monkeypatch.setattr(dual, "run_ssh_text", fake_run_ssh_text)
    monkeypatch.setattr(dual, "run_ssh_bytes", fake_run_ssh_bytes)

    result = dual.run_spectre_case(
        task_id="case",
        tb_path=tb_path,
        include_paths=[va_path],
        output_dir=output_dir,
        bridge_repo=tmp_path / "bridge",
        cadence_cshrc="/cadence.cshrc",
        timeout_s=5,
        side_output_files=("candidate.out",),
        spectre_backend="sui-direct",
        sui_host="thu-sui-test",
        sui_work_root="/tmp/vaevas-direct-spectre",
    )

    assert result["ok"] is True
    assert result["spectre_backend"] == "sui-direct"
    assert result["sui_host"] == "thu-sui-test"
    assert result["rows"] == 2
    assert result["signals"] == ["time", "out"]
    assert result["side_outputs"]["candidate.out"]["downloaded"] is True
    assert (output_dir / "tran_spectre.csv").exists()
    assert not (output_dir / "case__tb.ahdlSimDB").is_symlink()
    assert captured["uploaded_bytes"] > 0
    assert any("tcsh -c" in script for script in captured["text_scripts"])
    assert any('fallback_root="$HOME/WORK/vaevas-direct-spectre"' in script for script in captured["text_scripts"])
    assert any("_ahdlcmi_cache" in script and "ln -s" in script for script in captured["text_scripts"])
    assert result["ahdlcmi_cache"]["enabled"] is True
    assert result["ahdlcmi_cache"]["remote_cache_dir"].startswith("/tmp/vaevas-direct-spectre/_ahdlcmi_cache/")
    assert len(captured["unlock_scripts"]) == 1
    assert captured["unlock_scripts"][0].startswith("rmdir /tmp/vaevas-direct-spectre/_ahdlcmi_cache/")
    assert captured["unlock_scripts"][0].endswith(".lock")


def test_run_spectre_case_can_use_labctl_backend(monkeypatch, tmp_path: Path) -> None:
    output_dir = tmp_path / "out"
    tb_path = tmp_path / "tb.scs"
    va_path = tmp_path / "dut.va"
    tb_path.write_text('simulator lang=spectre\nahdl_include "dut.va"\n', encoding="utf-8")
    va_path.write_text("// stub dut\n", encoding="utf-8")
    psf_text = """HEADER
TYPE
SWEEP
TRACE
"time" "time"
"out" "voltage"
VALUE
"time" 0
"out" 0
"time" 1e-9
"out" 1
"""
    captured: dict[str, object] = {"commands": []}

    def fake_run_labctl(cmd, *, timeout_s):
        captured["commands"].append(cmd)
        if "up" in cmd:
            captured["upload_dir"] = cmd[cmd.index("up") + 1]
            captured["remote_dir"] = cmd[cmd.index("up") + 2]
            return SimpleNamespace(stdout="uploaded\n", stderr="", returncode=0)
        if "sh" in cmd:
            script_path = Path(cmd[cmd.index("sh") + 1])
            script_text = script_path.read_text(encoding="utf-8")
            if "cleanup" in script_path.name:
                captured["cleanup_script"] = script_text
                return SimpleNamespace(stdout="removed=/home/zhangz/WORK/vaevas-direct-spectre/case\n", stderr="", returncode=0)
            captured["run_script"] = script_text
            captured["spectre_line"] = cmd[-1]
            return SimpleNamespace(stdout="spectre completes\nTime used: elapsed = 1.5 s\n", stderr="", returncode=0)
        if "down" in cmd:
            local_dir = Path(cmd[cmd.index("down") + 2])
            if local_dir.exists():
                shutil.rmtree(local_dir)
            raw_dir = local_dir / "case__tb.raw"
            raw_dir.mkdir(parents=True)
            (raw_dir / "tran.tran.tran").write_text(psf_text, encoding="utf-8")
            (local_dir / "spectre.out").write_text(
                "Number of accepted tran steps = 2\nTime used: elapsed = 1.5 s\n",
                encoding="utf-8",
            )
            (local_dir / "candidate.out").write_text("side output\n", encoding="utf-8")
            return SimpleNamespace(stdout="downloaded\n", stderr="", returncode=0)
        raise AssertionError(f"unexpected labctl command: {cmd}")

    monkeypatch.setattr(dual, "run_labctl", fake_run_labctl)

    result = dual.run_spectre_case(
        task_id="case",
        tb_path=tb_path,
        include_paths=[va_path],
        output_dir=output_dir,
        bridge_repo=tmp_path / "bridge",
        cadence_cshrc="/cadence.cshrc",
        timeout_s=5,
        side_output_files=("candidate.out",),
        spectre_backend="labctl",
        sui_host="zhangz@101.6.68.147",
        sui_work_root="/home/zhangz/WORK/vaevas-direct-spectre",
    )

    assert result["ok"] is True
    assert result["spectre_backend"] == "labctl"
    assert result["labctl_host"] == "zhangz@101.6.68.147"
    assert result["rows"] == 2
    assert result["signals"] == ["time", "out"]
    assert result["side_outputs"]["candidate.out"]["downloaded"] is True
    assert (output_dir / "tran_spectre.csv").exists()
    commands = captured["commands"]
    assert any("--host" in cmd and "101.6.68.147" in cmd for cmd in commands)
    assert any("--user" in cmd and "zhangz" in cmd for cmd in commands)
    assert any(cmd[cmd.index("up")] == "up" for cmd in commands if "up" in cmd)
    assert any(cmd[cmd.index("down")] == "down" for cmd in commands if "down" in cmd)
    assert "/bin/csh -f __run_spectre.csh" in captured["run_script"]
    assert "spectre -64 case__tb.scs" in captured["spectre_line"]


def test_normalize_spectre_backend_accepts_labctl_aliases() -> None:
    assert dual.normalize_spectre_backend("labctl") == "labctl"
    assert dual.normalize_spectre_backend("lab") == "labctl"
    assert dual.normalize_spectre_backend("lab-ctl") == "labctl"


def test_direct_sui_ahdlcmi_cache_key_reuses_same_va_across_tb_labels(tmp_path: Path) -> None:
    out = tmp_path / "out"
    out.mkdir()
    tb_a = out / "task_visible__tb.scs"
    tb_b = out / "task_hidden__tb.scs"
    va = out / "dut.va"
    tb_a.write_text('ahdl_include "dut.va"\n', encoding="utf-8")
    tb_b.write_text('ahdl_include "dut.va"\ntran tran stop=2n\n', encoding="utf-8")
    va.write_text("module dut; endmodule\n", encoding="utf-8")

    key_a = dual.direct_sui_ahdlcmi_cache_key(
        input_files=[tb_a, va],
        output_dir=out,
        host="thu-wei",
        cadence_cshrc="/cadence.cshrc",
    )
    key_b = dual.direct_sui_ahdlcmi_cache_key(
        input_files=[tb_b, va],
        output_dir=out,
        host="thu-wei",
        cadence_cshrc="/cadence.cshrc",
    )
    assert key_a == key_b

    va.write_text("module dut; electrical out; endmodule\n", encoding="utf-8")
    key_changed = dual.direct_sui_ahdlcmi_cache_key(
        input_files=[tb_b, va],
        output_dir=out,
        host="thu-wei",
        cadence_cshrc="/cadence.cshrc",
    )
    assert key_changed != key_a


def test_copy_direct_spectre_inputs_rewrites_parent_solution_ahdl_include(tmp_path: Path) -> None:
    task_dir = tmp_path / "task"
    tb_dir = task_dir / "test_hidden"
    solution_dir = task_dir / "solution"
    output_dir = tmp_path / "out"
    tb_dir.mkdir(parents=True)
    solution_dir.mkdir()
    tb_path = tb_dir / "hidden.scs"
    dut_path = solution_dir / "generate_genvar_replicated_stage.vams"
    tb_path.write_text(
        'simulator lang=spectre\nahdl_include "../solution/generate_genvar_replicated_stage.vams"\n',
        encoding="utf-8",
    )
    dut_path.write_text("module generate_genvar_replicated_stage; endmodule\n", encoding="utf-8")

    staged_tb, copied = dual.copy_direct_spectre_inputs(
        task_id="449-generate-genvar-replicated-stage:hidden:gold",
        tb_path=tb_path,
        include_paths=[dut_path],
        output_dir=output_dir,
    )

    assert 'ahdl_include "generate_genvar_replicated_stage.vams"' in staged_tb.read_text(encoding="utf-8")
    assert "../solution" not in staged_tb.read_text(encoding="utf-8")
    assert output_dir / "generate_genvar_replicated_stage.vams" in copied


def test_copy_direct_spectre_inputs_stages_support_files_from_va_literals(tmp_path: Path) -> None:
    task_dir = tmp_path / "task"
    tb_dir = task_dir / "test_hidden"
    solution_dir = task_dir / "solution"
    output_dir = tmp_path / "out"
    tb_dir.mkdir(parents=True)
    solution_dir.mkdir()
    tb_path = tb_dir / "hidden.scs"
    dut_path = solution_dir / "noise_table_voltage_shaper.va"
    table_path = solution_dir / "noise_profile.tbl"
    tb_path.write_text(
        'simulator lang=spectre\nahdl_include "noise_table_voltage_shaper.va"\n',
        encoding="utf-8",
    )
    dut_path.write_text(
        'analog begin\n    V(out) <+ noise_table("noise_profile.tbl", "profile_noise");\nend\n',
        encoding="utf-8",
    )
    table_path.write_text("profile_noise 1 1\n", encoding="utf-8")

    _staged_tb, copied = dual.copy_direct_spectre_inputs(
        task_id="365-noise-table-voltage-shaper:hidden:gold",
        tb_path=tb_path,
        include_paths=[dut_path],
        output_dir=output_dir,
    )

    assert output_dir / "noise_profile.tbl" in copied
    assert (output_dir / "noise_profile.tbl").read_text(encoding="utf-8") == "profile_noise 1 1\n"


def test_direct_sui_backend_retries_transient_rc255(monkeypatch, tmp_path: Path) -> None:
    output_dir = tmp_path / "out"
    tb_path = tmp_path / "tb.scs"
    tb_path.write_text("simulator lang=spectre\n", encoding="utf-8")
    calls: list[dict[str, object]] = []

    monkeypatch.setenv("VAEVAS_SUI_DIRECT_RETRIES", "1")
    monkeypatch.setenv("VAEVAS_SUI_DIRECT_RETRY_BACKOFF_S", "0")

    def fake_direct(**kwargs):
        calls.append(kwargs)
        if len(calls) == 1:
            return {
                "ok": False,
                "status": "error",
                "errors": ["remote_upload_failed rc=255"],
                "warnings": [],
                "remote_run_dir": "/tmp/first",
            }
        return {
            "ok": True,
            "status": "success",
            "errors": [],
            "warnings": [],
            "remote_run_dir": "/tmp/second",
        }

    monkeypatch.setattr(dual, "run_spectre_case_sui_direct", fake_direct)

    result = dual.run_spectre_case(
        task_id="case",
        tb_path=tb_path,
        include_paths=[],
        output_dir=output_dir,
        bridge_repo=tmp_path / "bridge",
        cadence_cshrc="/cadence.cshrc",
        timeout_s=5,
        spectre_backend="sui-direct",
        sui_host="thu-sui-test",
        sui_work_root="/tmp/vaevas-direct-spectre",
    )

    assert result["ok"] is True
    assert len(calls) == 2
    assert result["sui_direct_retry_count"] == 1
    assert result["sui_direct_attempts"][0]["retryable"] is True
    assert "sui_direct_retry attempt=1 next_attempt=2 reason=remote_upload_failed rc=255" in result["warnings"][0]
    saved = json.loads((output_dir / "spectre_result.json").read_text(encoding="utf-8"))
    assert saved["sui_direct_retry_count"] == 1


def test_direct_sui_backend_does_not_retry_spectre_or_license_failure(monkeypatch, tmp_path: Path) -> None:
    output_dir = tmp_path / "out"
    tb_path = tmp_path / "tb.scs"
    tb_path.write_text("simulator lang=spectre\n", encoding="utf-8")
    calls: list[dict[str, object]] = []

    monkeypatch.setenv("VAEVAS_SUI_DIRECT_RETRIES", "3")

    def fake_direct(**kwargs):
        calls.append(kwargs)
        return {
            "ok": False,
            "status": "error",
            "errors": ["spectre_failed rc=1", "spectre_license_checkout_failed:SPECTRE-209"],
            "warnings": [],
            "remote_run_dir": "/tmp/fail",
        }

    monkeypatch.setattr(dual, "run_spectre_case_sui_direct", fake_direct)

    result = dual.run_spectre_case(
        task_id="case",
        tb_path=tb_path,
        include_paths=[],
        output_dir=output_dir,
        bridge_repo=tmp_path / "bridge",
        cadence_cshrc="/cadence.cshrc",
        timeout_s=5,
        spectre_backend="sui-direct",
        sui_host="thu-sui-test",
        sui_work_root="/tmp/vaevas-direct-spectre",
    )

    assert result["ok"] is False
    assert len(calls) == 1
    assert result["sui_direct_retry_count"] == 0
    assert result["sui_direct_attempts"][0]["retryable"] is False


def test_direct_sui_backend_reports_license_checkout_failure(monkeypatch, tmp_path: Path) -> None:
    output_dir = tmp_path / "out"
    tb_path = tmp_path / "tb.scs"
    va_path = tmp_path / "dut.va"
    tb_path.write_text('simulator lang=spectre\nahdl_include "dut.va"\n', encoding="utf-8")
    va_path.write_text("// stub dut\n", encoding="utf-8")
    captured: dict[str, object] = {"byte_calls": 0}

    def fake_run_ssh_text(host, script, *, timeout_s, input_data=None):
        captured.setdefault("text_scripts", []).append(script)
        if "mktemp" in script:
            return SimpleNamespace(stdout="/tmp/vaevas-direct-spectre/case.test\n", stderr="", returncode=0)
        if "AHDLCMI_CACHE_STATUS" in script:
            return SimpleNamespace(
                stdout=(
                    "AHDLCMI_LOCK_DIR=/tmp/vaevas-direct-spectre/_ahdlcmi_cache/key.lock\n"
                    "AHDLCMI_CACHE_STATUS=enabled\n"
                ),
                stderr="",
                returncode=0,
            )
        if script.startswith("rmdir "):
            return SimpleNamespace(stdout="", stderr="", returncode=0)
        if "rm -rf" in script:
            return SimpleNamespace(stdout="", stderr="", returncode=0)
        return SimpleNamespace(
            stdout=(
                "Fatal error found by spectre.\n"
                "FATAL (SPECTRE-209): Cannot run the simulation because the required license "
                "could not be checked out.\n"
            ),
            stderr="",
            returncode=1,
        )

    def fake_run_ssh_bytes(host, script, *, timeout_s, input_data=None):
        captured["byte_calls"] += 1
        assert input_data is not None
        return SimpleNamespace(stdout=b"", stderr=b"", returncode=0)

    monkeypatch.setattr(dual, "run_ssh_text", fake_run_ssh_text)
    monkeypatch.setattr(dual, "run_ssh_bytes", fake_run_ssh_bytes)

    result = dual.run_spectre_case(
        task_id="case",
        tb_path=tb_path,
        include_paths=[va_path],
        output_dir=output_dir,
        bridge_repo=tmp_path / "bridge",
        cadence_cshrc="/cadence.cshrc",
        timeout_s=5,
        spectre_backend="sui-direct",
        sui_host="thu-sui-test",
        sui_work_root="/tmp/vaevas-direct-spectre",
    )

    assert result["ok"] is False
    assert "spectre_failed rc=1" in result["errors"]
    assert "spectre_license_checkout_failed:SPECTRE-209" in result["errors"]
    assert not any(error.startswith("sui_direct_exception=ReadError") for error in result["errors"])
    assert captured["byte_calls"] == 1
