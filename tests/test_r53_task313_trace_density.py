from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
if str(RUNNERS) not in sys.path:
    sys.path.insert(0, str(RUNNERS))

from checkers.v4.task_313 import check_v4_313_dynamic_comparator_kickback_metric


NS = 1e-9


def _task313_rows(*, reset_never_clears: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []

    def add(
        time_ns: float,
        *,
        clk: float = 0.0,
        rst: float = 0.0,
        enable: float = 0.9,
        vinp: float = 0.52,
        vinn: float = 0.48,
        decision: float = 0.0,
        kickback_metric: float = 0.0,
        valid: float = 0.0,
    ) -> None:
        rows.append(
            {
                "time": time_ns * NS,
                "clk": clk,
                "rst": rst,
                "enable": enable,
                "vinp": vinp,
                "vinn": vinn,
                "decision": decision,
                "kickback_metric": kickback_metric,
                "valid": valid,
            }
        )

    add(0.0, rst=0.9, enable=0.0)
    add(0.3, rst=0.9, enable=0.0)
    add(1.0, rst=0.0, enable=0.9)

    previous = (0.0, 0.0, 0.0)
    decisions = [
        (0.52, 0.48),
        (0.46, 0.52),
        (0.78, 0.24),
        (0.20, 0.58),
        (0.62, 0.54),
        (0.42, 0.58),
    ]
    for edge_ns, (vinp, vinn) in zip((10.0, 20.0, 30.0, 40.0), decisions):
        decision, metric, valid = previous
        add(edge_ns - 0.1, vinp=vinp, vinn=vinn, decision=decision, kickback_metric=metric, valid=valid)
        add(edge_ns, clk=0.9, vinp=vinp, vinn=vinn, decision=decision, kickback_metric=metric, valid=valid)
        overdrive = abs(vinp - vinn)
        target = (1.0 if vinp >= vinn else 0.0, 0.45 + 0.30 / (1.0 + overdrive / 0.030), 0.9)
        add(edge_ns + 0.2, clk=0.9, vinp=vinp, vinn=vinn, decision=target[0], kickback_metric=target[1], valid=target[2])
        add(edge_ns + 1.0, vinp=vinp, vinn=vinn, decision=target[0], kickback_metric=target[1], valid=target[2])
        add(edge_ns + 1.6, vinp=vinp, vinn=vinn, decision=target[0], kickback_metric=target[1], valid=target[2])
        previous = target

    decision, metric, valid = previous
    add(43.00, rst=0.36, decision=decision, kickback_metric=metric, valid=valid)
    add(43.10, rst=0.54, decision=decision, kickback_metric=metric, valid=valid)
    add(43.12, rst=0.9, decision=decision * 0.7, kickback_metric=metric * 0.7, valid=valid * 0.7)
    if reset_never_clears:
        add(43.249, rst=0.9, decision=decision, kickback_metric=metric, valid=valid)
        add(43.251, rst=0.9, decision=decision, kickback_metric=metric, valid=valid)
    else:
        add(43.249, rst=0.9, decision=decision, kickback_metric=metric, valid=valid)
        add(43.251, rst=0.9)
    add(44.20, rst=0.0)
    previous = (0.0, 0.0, 0.0)

    for edge_ns, (vinp, vinn) in zip((50.0, 60.0), decisions[4:]):
        decision, metric, valid = previous
        add(edge_ns - 0.1, vinp=vinp, vinn=vinn, decision=decision, kickback_metric=metric, valid=valid)
        add(edge_ns, clk=0.9, vinp=vinp, vinn=vinn, decision=decision, kickback_metric=metric, valid=valid)
        overdrive = abs(vinp - vinn)
        target = (1.0 if vinp >= vinn else 0.0, 0.45 + 0.30 / (1.0 + overdrive / 0.030), 0.9)
        add(edge_ns + 0.2, clk=0.9, vinp=vinp, vinn=vinn, decision=target[0], kickback_metric=target[1], valid=target[2])
        add(edge_ns + 1.0, vinp=vinp, vinn=vinn, decision=target[0], kickback_metric=target[1], valid=target[2])
        add(edge_ns + 1.6, vinp=vinp, vinn=vinn, decision=target[0], kickback_metric=target[1], valid=target[2])
        previous = target

    add(67.0, enable=0.0)
    add(68.0, enable=0.0)
    return rows


def test_task313_allows_public_transition_settling_after_reset_assertion() -> None:
    ok, note = check_v4_313_dynamic_comparator_kickback_metric(_task313_rows())
    assert ok, note
    assert "late_reset_violation=False" in note


def test_task313_still_rejects_outputs_that_do_not_clear_after_reset_settling() -> None:
    ok, note = check_v4_313_dynamic_comparator_kickback_metric(
        _task313_rows(reset_never_clears=True)
    )
    assert not ok, note
    assert "late_reset_violation=True" in note
