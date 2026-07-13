# Bin2ther 2b Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Bin2ther 2b` DUT. The evaluator runs the same submitted bytes
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

- `P_INTERPRET_B1_AND_B0_RELATIVE_TO`: Interpret `b1` and `b0` relative to the local rail midpoint.
- `P_DRIVE_T0_AND_T1_HIGH_TOGETHER`: Drive `t0` and `t1` high together when `b1` is high.
- `P_DRIVE_T2_HIGH_WHEN_B0_IS`: Drive `t2` high when `b0` is high.
- `P_DRIVE_EACH_LOW_OUTPUT_TO_THE`: Drive each low output to the local `gnd` rail and each high output to the local `vdd` rail.

The required trace names are: `time`, `vdd`, `gnd`, `b1`, `b0`, `t0`, `t1`, `t2`.

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
