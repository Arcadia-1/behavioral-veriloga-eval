# Op-amp Feedback Settling Monitor Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Op-amp Feedback Settling Monitor` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_OR_WHEN_ENABLE_IS`: On reset or when `enable` is low, drive `vout` to `vcm`, clear `error_metric`, and clear `settled`.
- `P_DECODE_GAIN_2_GAIN_0_INTO`: Decode `gain_2..gain_0` into a closed-loop target gain of at least unity.
- `P_UPDATE_VOUT_ONCE_PER_RISING_CLK`: Update `vout` once per rising `clk` edge toward the target closed-loop output using `alpha`.
- `P_CLAMP_VOUT_TO_THE_RANGE_VSS`: Clamp `vout` to the range `vss` through `vdd`.
- `P_ERROR_METRIC_MUST_EXPOSE_THE_SIGNED`: `error_metric` must expose the signed difference between the current output and the target closed-loop value.
- `P_ASSERT_SETTLED_AFTER_THREE_CONSECUTIVE_UPDATES`: Assert `settled` after three consecutive updates where the absolute error is below `settle_tol`.

The required trace names are: `time`, `vin`, `clk`, `rst`, `enable`, `gain_2`, `gain_1`, `gain_0`, `vout`, `error_metric`, `settled`.

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
