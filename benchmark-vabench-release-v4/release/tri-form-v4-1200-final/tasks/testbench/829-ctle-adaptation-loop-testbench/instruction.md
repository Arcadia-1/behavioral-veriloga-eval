# CTLE Adaptation Loop Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `CTLE Adaptation Loop` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear boost code, output, metric, and `locked`.
- `P_ON_EACH_ENABLED_RISING_CLK_EDGE`: On each enabled rising `clk` edge, compare `edge_metric_in` with `edge_target`.
- `P_INCREASE_BOOST_CODE_WHEN_EDGE_METRIC`: Increase boost code when edge metric is too low and decrease it when too high.
- `P_DRIVE_VOUT_AS_A_BOOSTED_VERSION`: Drive `vout` as a boosted version of `vin - vcm` using the active boost code.
- `P_ASSERT_LOCKED_AFTER_THREE_CONSECUTIVE_UPDATES`: Assert `locked` after three consecutive updates within the target tolerance.

The required trace names are: `time`, `vin`, `edge_metric_in`, `clk`, `rst`, `enable`, `boost_2`, `boost_1`, `boost_0`, `vout`, `adapt_metric`, `locked`.

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
