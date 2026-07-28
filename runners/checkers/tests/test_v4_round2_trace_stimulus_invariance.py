from __future__ import annotations

from runners.checkers.v4.task_052 import CHECKER as checker_052
from runners.checkers.v4.task_085 import CHECKER as checker_085
from runners.checkers.v4.task_087 import CHECKER as checker_087
from runners.checkers.v4.task_098 import CHECKER as checker_098
from runners.checkers.v4.task_130 import CHECKER as checker_130
from runners.checkers.v4.task_217 import CHECKER as checker_217
from runners.checkers.v4.task_368 import CHECKER as checker_368
from runners.checkers.v4.task_387 import CHECKER as checker_387


VDD = 0.9


def _duplicate_rows(rows: list[dict[str, float]]) -> list[dict[str, float]]:
    return [copy for row in rows for copy in (row.copy(), row.copy())]


def _thermometer_row(time: float, vin: float, code: int) -> dict[str, float]:
    row = {"time": time, "vin": vin}
    row.update({f"t{bit}": VDD if bit < code else 0.0 for bit in range(16)})
    return row


def _task052_rows(*, wrong_endpoint: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    time = 0.0
    plateaus = ((0.02, 0), (0.22, 3), (0.51, 8), (0.88, 14), (1.05, 16))
    for index, (vin, code) in enumerate(plateaus):
        if index:
            previous_vin, previous_code = plateaus[index - 1]
            rows.append(_thermometer_row(time, 0.5 * (previous_vin + vin), previous_code))
            time += 20e-12
        observed_code = 15 if wrong_endpoint and index == len(plateaus) - 1 else code
        rows.extend(
            _thermometer_row(time + offset, vin, observed_code)
            for offset in (0.0, 0.4e-9, 0.8e-9)
        )
        time += 1.0e-9
    return rows


def _task085_rows(*, samples: int, valid_missing: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for index in range(samples):
        fraction = index / (samples - 1)
        inp = 0.49 + 0.03 * fraction
        captured = inp >= 0.505
        rows.append(
            {
                "time": 100e-9 * fraction,
                "inp": inp,
                "inn": 0.5,
                "outp": VDD if captured else 0.0,
                "trip_v": 0.505 if captured else 0.0,
                "offset_est": 0.005 if captured else 0.0,
                "valid": 0.0 if valid_missing else (VDD if captured else 0.0),
            }
        )
    return rows


_RECON = (0.000, 0.055, 0.118, 0.182, 0.245, 0.303, 0.366, 0.428,
          0.491, 0.553, 0.612, 0.674, 0.735, 0.798, 0.855, 0.900)


def _task087_rows(*, recon_defect: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    previous_code: int | None = None
    previous_recon: float | None = None
    for code, recon in enumerate(_RECON):
        time = code * 4e-9
        observed_recon = 0.0 if recon_defect and code >= 8 else recon
        ideal = 0.06 * code
        inl = max(0.05, min(0.85, 0.45 + 3.0 * (observed_recon - ideal)))
        if previous_code is not None and previous_recon is not None:
            dnl = 0.45 + 4.0 * ((observed_recon - previous_recon) - 0.06 * (code - previous_code))
        else:
            dnl = 0.45
        dnl = max(0.05, min(0.85, dnl))
        common = {
            "rst": 0.0,
            "vin": ideal,
            "code": ideal,
            "recon": observed_recon,
            "dnl": dnl,
            "inl": inl,
        }
        rows.append({"time": time, "clk": 0.0, **common})
        rows.append({"time": time + 0.1e-9, "clk": VDD, **common})
        rows.append({"time": time + 0.8e-9, "clk": VDD, **common})
        previous_code = code
        previous_recon = observed_recon
    return rows


def _task098_rows(*, cycle_count: int = 200, dense: bool = False) -> list[dict[str, float]]:
    rows = [{"time": 0.0, "CLK": 0.0}]
    time = 0.0
    for cycle in range(cycle_count):
        period = 20e-9 if cycle < 100 else 19.5e-9
        rows.append({"time": time + 0.20 * period, "CLK": 0.0})
        rows.append({"time": time + 0.25 * period, "CLK": VDD})
        if dense:
            rows.append({"time": time + 0.45 * period, "CLK": VDD})
        rows.append({"time": time + 0.70 * period, "CLK": VDD})
        rows.append({"time": time + 0.75 * period, "CLK": 0.0})
        time += period
    rows.append({"time": time, "CLK": 0.0})
    return rows


def _task130_rows(*, include_zero_sample: bool, polarity_defect: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    sigref = 0.45
    samples: list[tuple[float, float]] = []
    for index in range(10):
        samples.append((index * 0.1e-9, 0.25))
    for index in range(10):
        samples.append((1.0e-9 + index * 0.1e-9, 0.18))
    if include_zero_sample:
        for index in range(4):
            samples.append((2.0e-9 + index * 0.1e-9, 0.0))
    for index in range(10):
        samples.append((2.4e-9 + index * 0.1e-9, -0.16))
    for index in range(10):
        samples.append((3.4e-9 + index * 0.1e-9, -0.22))
    for time, diff in samples:
        sigin_p = sigref + 0.5 * diff
        sigin_n = sigref - 0.5 * diff
        sigout_p = sigref + diff
        sigout_n = sigref - diff
        if polarity_defect:
            sigout_p, sigout_n = sigout_n, sigout_p
        rows.append(
            {
                "time": time,
                "sigin_p": sigin_p,
                "sigin_n": sigin_n,
                "sigout_p": sigout_p,
                "sigout_n": sigout_n,
                "sigref": sigref,
            }
        )
    return rows


def _task217_rows(*, step: float, missing_final_fall: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    trigger_times = (0.62e-9, 3.62e-9)
    time = 0.0
    while time <= 5.8e-9 + step / 2:
        vin_high = any(edge <= time < edge + 0.6e-9 for edge in trigger_times)
        output_high = any(
            edge + 0.10e-9 <= time < (5.9e-9 if missing_final_fall and edge == trigger_times[-1] else edge + 2.10e-9)
            for edge in trigger_times
        )
        rows.append({"time": time, "vin": VDD if vin_high else 0.0, "vout": VDD if output_high else 0.0})
        time += step
    return rows


def _task368_rows(*, samples_per_window: int, amp_defect: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    time = 0.0
    valid_count = 0
    previous_clk = 0.0
    windows = (
        (0.45, False, True, 0.0, 0.0),
        (0.70, True, False, 0.0, VDD),
        (0.20, True, False, VDD, 0.0),
        (0.70, True, False, 0.0, VDD),
        (0.46, True, False, VDD, 0.0),
        (0.20, True, False, 0.0, VDD),
        (0.45, False, False, 0.0, 0.0),
        (0.45, False, True, 0.0, 0.0),
    )
    for vin, enabled, reset, clk_start, clk_end in windows:
        raw = 4.0 * (vin - 0.45)
        limited = max(-0.35, min(0.35, raw))
        amp = abs(limited)
        for index in range(samples_per_window):
            fraction = index / (samples_per_window - 1)
            clk = clk_start if fraction < 0.5 else clk_end
            rising = previous_clk <= 0.45 < clk
            if not enabled or reset:
                valid_count = 0
            elif rising:
                valid_count = valid_count + 1 if amp >= 0.040 else 0
            active = enabled and not reset
            rows.append(
                {
                    "time": time + 2e-9 * fraction,
                    "vin_proxy": vin,
                    "rst": VDD if reset else 0.0,
                    "enable": VDD if enabled else 0.0,
                    "clk": clk,
                    "vout": 0.45 + limited if active else 0.45,
                    "decision": VDD if active and limited >= 0.0 else 0.0,
                    "limit_flag": VDD if active and abs(raw) > 0.35 else 0.0,
                    "valid": VDD if active and valid_count >= 2 else 0.0,
                    "amp_metric": (0.0 if amp_defect and active else amp) if active else 0.0,
                }
            )
            previous_clk = clk
        time += 2e-9
    return rows


def _task387_rows(*, samples_per_plateau: int, bad_flag: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    plateaus = (
        (True, True, 0.45),
        (False, False, 0.45),
        (False, True, 0.50),
        (False, True, 0.85),
    )
    for plateau, (reset, enabled, vin) in enumerate(plateaus):
        excess = max(0.0, abs(vin - 0.45) - 0.18)
        gain = 4.0 / (1.0 + excess / 0.20)
        active = enabled and not reset
        compressed = active and gain < 3.4
        for sample in range(samples_per_plateau):
            fraction = sample / (samples_per_plateau - 1)
            rows.append(
                {
                    "time": (1.2 * plateau + fraction) * 1e-9,
                    "rst": VDD if reset else 0.0,
                    "enable": VDD if enabled else 0.0,
                    "vin": vin,
                    "vout": max(0.0, min(VDD, 0.45 + gain * (vin - 0.45))) if active else 0.45,
                    "gain_metric": max(0.0, min(VDD, VDD * gain / 4.0)) if active else 0.0,
                    "compression_flag": 0.0 if bad_flag and compressed else (VDD if compressed else 0.0),
                }
            )
    return rows


def test_052_sparse_dense_and_duplicate_equivalents_pass_but_endpoint_mutation_fails() -> None:
    reference = _task052_rows()
    for rows in (reference, reference[::2] + [reference[-1]], _duplicate_rows(reference)):
        ok, note = checker_052(rows)
        assert ok, note
    assert not checker_052(_duplicate_rows(_task052_rows(wrong_endpoint=True)))[0]


def test_085_plateau_density_is_invariant_and_missing_valid_is_rejected() -> None:
    for rows in (_task085_rows(samples=41), _task085_rows(samples=201), _duplicate_rows(_task085_rows(samples=41))):
        ok, note = checker_085(rows)
        assert ok, note
    assert not checker_085(_task085_rows(samples=41, valid_missing=True))[0]


def test_087_duplicate_publication_is_invariant_and_reconstruction_mutation_fails() -> None:
    reference = _task087_rows()
    for rows in (reference, _duplicate_rows(reference)):
        ok, note = checker_087(rows)
        assert ok, note
    assert not checker_087(_task087_rows(recon_defect=True))[0]


def test_098_sparse_dense_and_duplicate_clocks_agree_while_two_edge_trace_fails() -> None:
    for rows in (_task098_rows(), _task098_rows(dense=True), _duplicate_rows(_task098_rows())):
        ok, note = checker_098(rows)
        assert ok, note
    assert not checker_098(_task098_rows(cycle_count=2))[0]


def test_130_region_coverage_accepts_sparse_pwl_zero_crossing_but_rejects_polarity_defect() -> None:
    for rows in (
        _task130_rows(include_zero_sample=True),
        _task130_rows(include_zero_sample=False),
        _duplicate_rows(_task130_rows(include_zero_sample=False)),
    ):
        ok, note = checker_130(rows)
        assert ok, note
    assert not checker_130(_task130_rows(include_zero_sample=False, polarity_defect=True))[0]


def test_217_sparse_dense_and_duplicate_pulses_agree_while_missing_tail_fails() -> None:
    for rows in (_task217_rows(step=0.05e-9), _task217_rows(step=0.08e-9), _duplicate_rows(_task217_rows(step=0.08e-9))):
        ok, note = checker_217(rows)
        assert ok, note
    assert not checker_217(_task217_rows(step=0.05e-9, missing_final_fall=True))[0]


def test_368_sparse_dense_and_duplicate_plateaus_agree_while_amp_mutation_fails() -> None:
    for rows in (_task368_rows(samples_per_window=8), _task368_rows(samples_per_window=36), _duplicate_rows(_task368_rows(samples_per_window=8))):
        ok, note = checker_368(rows)
        assert ok, note
    assert not checker_368(_task368_rows(samples_per_window=8, amp_defect=True))[0]


def test_387_semantic_plateau_coverage_is_density_invariant_and_bad_flag_fails() -> None:
    for rows in (
        _task387_rows(samples_per_plateau=2),
        _task387_rows(samples_per_plateau=12),
        _duplicate_rows(_task387_rows(samples_per_plateau=2)),
    ):
        ok, note = checker_387(rows)
        assert ok, note
    assert not checker_387(_task387_rows(samples_per_plateau=2, bad_flag=True))[0]
