# Image-reject Mixer Calibration Loop Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Image-reject Mixer Calibration Loop` DUT. The evaluator runs the same submitted bytes
against the correct DUT and five anonymous semantic negative DUTs. Your
testbench must accept the correct DUT and expose all five behavioral faults.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

The exact read-only source paths, modules, ports, instance names, and ordered
terminal bindings are declared in `solver_contract.json`.

## Public Parameter Contract

Honor the public parameter declarations in `solver_contract.json` when choosing
stimulus and coverage.

## Required Behavior

Create stimulus and save traces sufficient for the fixed evaluator oracle to check:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear I/Q outputs to `vcm`, image metric to `vss`, and `calibrated` to `vss`; the disabled interval should occur after nonzero mixer/calibration state has been produced so the clear is observable.
- `P_ON_EACH_ENABLED_RISING_CLK_EDGE`: On each enabled rising `clk` edge, sample the current RF and quadrature LO input voltages; use stimulus values that differ between rising and falling crossings to distinguish the intended sampling edge.
- `P_GENERATE_I_AND_Q_OUTPUTS_USING`: Generate I and Q outputs from `rf_dev = rf_in-vcm` and LO signs decoded around `vth`: before correction I follows `rf_dev*lo_i_sign` while Q follows the opposite-polarity path `-rf_dev*lo_q_sign`; exercise RF above/below `vcm` and both LO signs.
- `P_UPDATE_A_SIMPLE_GAIN_PHASE_CORRECTION`: Update bounded gain/phase correction state away from `vcm` when the raw image metric is above `image_tol`, and decay corrections toward `vcm` when the image metric is below tolerance; the stimulus should make wrong correction direction increase or fail to reduce the public image metric.
- `P_ASSERT_CALIBRATED_AFTER_THREE_CONSECUTIVE_UPDA`: Assert `calibrated` only after the third consecutive enabled update with image metric below `image_tol`; the first and second below-tolerance updates, reset, and disabled intervals must leave it deasserted.

The required trace names are: `time`, `rf_in`, `lo_i`, `lo_q`, `clk`, `rst`, `enable`, `i_out`, `q_out`, `image_metric`, `calibrated`.

## Modeling Constraints

- Submit one self-contained top-level transient `.scs` file.
- Use only the exact declared testbench include paths and public DUT interfaces.
- Do not redefine the DUT, drive declared DUT outputs, inspect private internals,
  access undeclared files, or emit a self-reported result.
- Respect every public resource limit in `solver_contract.json`.
- Missing traces, setup errors, and invalid runs do not count as behavioral kills.

## Output Contract

Return exactly one submission-root-relative artifact named `testbench.scs`. Do not return a DUT,
checker, script, data file, waveform, or auxiliary deck.
