import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "run_v4_stimulus_metamorphic.py"
SPEC = importlib.util.spec_from_file_location("run_v4_stimulus_metamorphic", MODULE_PATH)
assert SPEC and SPEC.loader
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


def test_affine_transform_scales_pwl_and_shifts_absolute_times() -> None:
    deck = (
        "Vx (x 0) vsource type=pwl wave=[0 0 10n 0.9]\n"
        "Vclk (clk 0) vsource type=pulse period=5n width=2n delay=1n rise=10p fall=20p\n"
        "XDUT (x) dut unit_phase_delay=40p tr=20p\n"
        "tran tran stop=20n maxstep=100p\n"
    )
    transformed = runner.transform_stimulus(deck, scale=2.0, shift=1e-9)
    assert "wave=[1n 0 21n 0.9]" in transformed
    assert "period=10n" in transformed
    assert "width=4n" in transformed
    assert "delay=3n" in transformed
    assert "rise=20p" in transformed
    assert "fall=40p" in transformed
    assert "unit_phase_delay=80p" in transformed
    assert "tr=40p" in transformed
    assert "stop=41n" in transformed
    assert "maxstep=200p" in transformed


def test_insufficient_stimulus_keeps_legal_source_declarations() -> None:
    deck = "Vx (x 0) vsource type=pwl wave=[0 0 5n 0.9]\nVclk (c 0) vsource type=pulse period=5n width=2n\n"
    suppressed = runner.suppress_stimulus(deck)
    assert "type=pwl" not in suppressed
    assert "type=pulse" not in suppressed
    assert suppressed.count("vsource dc=0") == 2
