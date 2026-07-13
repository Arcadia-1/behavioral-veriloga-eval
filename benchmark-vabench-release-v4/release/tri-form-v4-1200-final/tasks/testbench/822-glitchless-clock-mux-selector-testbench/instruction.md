# Glitchless Clock Mux Selector Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Glitchless Clock Mux Selector` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive `clk_out`, `switch_metric`, and `valid` low.
- `P_ROUTE_CLK_A_WHEN_SEL_IS`: Route `clk_a` when `sel` is low and `clk_b` when `sel` is high.
- `P_WHEN_SEL_CHANGES_WAIT_UNTIL_BOTH`: When `sel` changes, wait until both input clocks are low before changing the active source.
- `P_EXPOSE_A_SWITCH_EVENT_ON_SWITCH`: Expose a switch event on `switch_metric` for one output cycle after the selected source changes.
- `P_ASSERT_VALID_AFTER_THE_SELECTED_SOURCE`: Assert `valid` after the selected source has produced one clean output edge.

The required trace names are: `time`, `clk_a`, `clk_b`, `sel`, `rst`, `enable`, `clk_out`, `switch_metric`, `valid`.

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
