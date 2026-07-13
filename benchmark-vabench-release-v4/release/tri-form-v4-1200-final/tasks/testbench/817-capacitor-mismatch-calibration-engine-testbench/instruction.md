# Capacitor Mismatch Calibration Engine Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Capacitor Mismatch Calibration Engine` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear the calibration code, metric, and `done`.
- `P_ON_EACH_ENABLED_RISING_CLK_EDGE`: On each enabled rising `clk` edge, update a signed correction accumulator using the sign of `err_in - vcm`.
- `P_SATURATE_THE_PUBLIC_4_BIT_CALIBRATION`: Saturate the public 4-bit calibration code at the endpoints.
- `P_DRIVE_CORRECTION_METRIC_AS_THE_VOLTAGE`: Drive `correction_metric` as the voltage-coded correction applied by the active code.
- `P_ASSERT_DONE_AFTER_EIGHT_ENABLED_UPDATES`: Assert `done` after eight enabled updates or when the error remains within `err_tol` for two updates.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

The required trace names are: `time`, `err_in`, `clk`, `rst`, `enable`, `cal_3`, `cal_2`, `cal_1`, `cal_0`, `correction_metric`, `done`.

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
