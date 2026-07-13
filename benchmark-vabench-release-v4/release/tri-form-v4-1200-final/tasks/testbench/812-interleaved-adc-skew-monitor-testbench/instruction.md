# Interleaved ADC Timing-skew Monitor Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Interleaved ADC Timing-skew Monitor` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear both sample states and all metrics.
- `P_CAPTURE_VIN_A_ON_RISING_CLK`: Capture `vin_a` on rising `clk_a` and `vin_b` on rising `clk_b`.
- `P_ESTIMATE_A_SKEW_PROXY_FROM_THE`: Estimate a skew proxy from the signed difference between the two most recent samples.
- `P_DRIVE_SKEW_METRIC_WITH_THE_ABSOLUTE`: Drive `skew_metric` with the absolute skew proxy and `magnitude_metric` with the average sample magnitude.
- `P_ASSERT_ALARM_WHEN_SKEW_METRIC_EXCEEDS`: Assert `alarm` when `skew_metric` exceeds `skew_limit` for two consecutive comparisons.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

The required trace names are: `time`, `vin_a`, `vin_b`, `clk_a`, `clk_b`, `rst`, `enable`, `skew_metric`, `magnitude_metric`, `alarm`.

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
