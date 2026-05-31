from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN_WITH_BRIDGE = ROOT / "scripts" / "run_with_bridge.sh"
START_TUNNEL = ROOT / "scripts" / "start_bridge_tunnel.sh"


def test_bridge_scripts_fail_fast_on_unreachable_ssh() -> None:
    for script in (RUN_WITH_BRIDGE, START_TUNNEL):
        text = script.read_text(encoding="utf-8")
        assert "ConnectTimeout" in text
        assert "ServerAliveInterval" in text
        assert "ServerAliveCountMax" in text


def test_bridge_scripts_support_profiled_env_overrides() -> None:
    for script in (RUN_WITH_BRIDGE, START_TUNNEL):
        text = script.read_text(encoding="utf-8")
        assert "BRIDGE_PROFILE" in text
        assert "apply_bridge_profile" in text
        assert "VB_REMOTE_HOST VB_REMOTE_USER VB_JUMP_HOST VB_JUMP_USER VB_REMOTE_PORT VB_LOCAL_PORT VB_CADENCE_CSHRC VB_USE_SSH_CONFIG_JUMP" in text
        assert "--profile" in text
        assert "VB_USE_SSH_CONFIG_JUMP" in text
        assert "using ssh_config ProxyJump route" in text


def test_release_rerun_wrapper_writes_structured_blocker_on_tunnel_failure() -> None:
    text = RUN_WITH_BRIDGE.read_text(encoding="utf-8")

    assert "failed to start temporary bridge tunnel" in text
    assert "runners/run_vabench_release_dual_rerun.py" in text
    assert "VAEVAS_BRIDGE_FAILURE_REASON" in text
    assert "--allow-direct-run" not in text
    assert "bridge_preflight.py" in text


def test_start_tunnel_reports_preflight_on_tunnel_failure() -> None:
    text = START_TUNNEL.read_text(encoding="utf-8")

    assert "failed to start bridge tunnel" in text
    assert "bridge_preflight.py" in text
    assert "exit 1" in text
