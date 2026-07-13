# Baseband Anti-alias Filter Macro Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Baseband Anti-alias Filter Macro` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive `vout` to `vcm`, clear metric, and clear `valid`.
- `P_ON_EACH_ENABLED_RISING_CLK_EDGE`: On each enabled rising `clk` edge, decode `bw_1..bw_0` as a bandwidth setting.
- `P_UPDATE_VOUT_AS_A_FIRST_ORDER`: Update `vout` as a first-order discrete-time low-pass response to `vin`.
- `P_HIGHER_BANDWIDTH_CODE_MUST_MOVE_VOUT`: Higher bandwidth code must move `vout` closer to `vin` per update.
- `P_EXPOSE_THE_ACTIVE_BANDWIDTH_CODE_ON`: Expose the active bandwidth code on `bandwidth_metric` and assert `valid` after the first update.

The required trace names are: `time`, `vin`, `clk`, `rst`, `enable`, `bw_1`, `bw_0`, `vout`, `bandwidth_metric`, `valid`.

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
