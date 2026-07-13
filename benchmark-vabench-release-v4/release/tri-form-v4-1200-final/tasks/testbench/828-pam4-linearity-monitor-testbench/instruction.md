# PAM4 Linearity Monitor Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `PAM4 Linearity Monitor` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear output, metric, and `valid`.
- `P_ON_EACH_ENABLED_RISING_CLK_EDGE`: On each enabled rising `clk` edge, decode `symbol_1..symbol_0` as one of four PAM4 levels.
- `P_DRIVE_LEVEL_OUT_TO_EVENLY_SPACED`: Drive `level_out` to evenly spaced voltage levels between `vss` and `vdd`.
- `P_EXPOSE_A_LINEARITY_METRIC_THAT_IS`: Expose a `linearity_metric` that is high only when adjacent level spacing is uniform.
- `P_ASSERT_VALID_AFTER_EACH_SAMPLED_SYMBOL`: Assert `valid` after each sampled symbol update.

The required trace names are: `time`, `symbol_1`, `symbol_0`, `clk`, `rst`, `enable`, `level_out`, `linearity_metric`, `valid`.

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
