# Thermal Foldback Power Limiter Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Thermal Foldback Power Limiter` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear limited command, foldback metric, and status.
- `P_ON_EACH_ENABLED_RISING_CLK_EDGE`: On each enabled rising `clk` edge, compare `temp_sense` against the foldback threshold.
- `P_PASS_POWER_CMD_THROUGH_WHILE_TEMPERATURE`: Pass `power_cmd` through while temperature is below threshold.
- `P_REDUCE_LIMITED_CMD_AS_TEMPERATURE_RISES`: Reduce `limited_cmd` as temperature rises above threshold and expose the reduction on `foldback_metric`.
- `P_ASSERT_THERMAL_OK_ONLY_WHEN_NO`: Assert `thermal_ok` only when no foldback reduction is active.

The required trace names are: `time`, `power_cmd`, `temp_sense`, `clk`, `rst`, `enable`, `limited_cmd`, `foldback_metric`, `thermal_ok`.

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
