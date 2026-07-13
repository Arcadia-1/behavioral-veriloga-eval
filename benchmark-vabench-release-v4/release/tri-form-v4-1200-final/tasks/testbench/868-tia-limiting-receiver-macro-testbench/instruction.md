# TIA Limiting Receiver Macro Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `TIA Limiting Receiver Macro` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_OR_WHEN_ENABLE_IS`: On reset or when `enable` is low, drive `vout` to `vcm` and clear `decision`, `limit_flag`, `valid`, and `amp_metric`.
- `P_TREAT_VIN_PROXY_AS_A_VOLTAGE`: Treat `vin_proxy` as a voltage-domain proxy for receiver input magnitude; no current ports are required.
- `P_APPLY_GAIN_TO_THE_DEVIATION_FROM`: Apply gain to the deviation from `vcm` and clamp the output to `vcm +/- limit`.
- `P_ASSERT_LIMIT_FLAG_WHEN_THE_UNCLAMPED`: Assert `limit_flag` when the unclamped amplified signal would exceed the limiter range.
- `P_ON_EACH_RISING_CLK_EDGE_DRIVE`: On each rising `clk` edge, drive `decision` high when the limited output is at or above `vcm`, otherwise low.
- `P_ASSERT_VALID_WHEN_AMP_METRIC_IS`: Assert `valid` when `amp_metric` is at least `valid_min` for two consecutive clock updates.

The required trace names are: `time`, `vin_proxy`, `clk`, `rst`, `enable`, `vout`, `decision`, `limit_flag`, `valid`, `amp_metric`.

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
