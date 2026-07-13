# SST Driver Impedance Macro Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `SST Driver Impedance Macro` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_DISABLE_CLEAR`: Reset or low enable drives common mode and clears public metrics.
- `P_CLOCKED_DATA`: The data decision updates only on enabled rising clock edges.
- `P_SWING_MAPPING`: The trim code selects swing_min plus swing_lsb per code step.
- `P_DATA_POLARITY`: High and low latched data drive equal-polarity swings around VCM.
- `P_TRIM_METRIC`: The trim metric maps unsigned codes 0 and 7 to the public rails linearly.

The required trace names are: `time`, `data`, `enable`, `clk`, `rst`, `z_2`, `z_1`, `z_0`, `vout`, `swing_metric`, `z_metric`.

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
