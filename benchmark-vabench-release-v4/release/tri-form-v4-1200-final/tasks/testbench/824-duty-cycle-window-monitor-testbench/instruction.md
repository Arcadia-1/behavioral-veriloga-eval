# Duty-cycle Window Monitor Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Duty-cycle Window Monitor` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear duty metric, window flag, and `valid`.
- `P_MEASURE_HIGH_AND_LOW_INTERVALS_OVER`: Measure high and low intervals over complete clock cycles using threshold crossings.
- `P_DRIVE_DUTY_METRIC_AS_THE_MEASURED`: Drive `duty_metric` as the measured high-time fraction mapped to the public voltage range.
- `P_ASSERT_IN_WINDOW_ONLY_WHEN_THE`: Assert `in_window` only when the measured duty lies between `duty_min` and `duty_max`.
- `P_ASSERT_VALID_AFTER_A_COMPLETE_HIGH`: Assert `valid` after a complete high/low cycle has been observed.

The required trace names are: `time`, `clk_in`, `rst`, `enable`, `duty_min`, `duty_max`, `duty_metric`, `in_window`, `valid`.

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
