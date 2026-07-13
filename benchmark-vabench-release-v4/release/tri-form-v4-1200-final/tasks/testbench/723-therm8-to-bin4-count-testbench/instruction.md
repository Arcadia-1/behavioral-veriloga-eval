# Therm8 To Bin4 Count Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Therm8 To Bin4 Count` DUT. The evaluator runs the same submitted bytes
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

- `P_COUNT_HOW_MANY_OF_TH0_TH7`: Count how many of `th0..th7` are above `vth`.
- `P_ENCODE_THE_COUNT_AS_A_4`: Encode the count as a 4-bit binary word.
- `P_DRIVE_B0_B3_AS_VOLTAGE_CODED`: Drive `b0..b3` as voltage-coded outputs with `b0` as the least significant bit.
- `P_SUPPORT_ANY_INPUT_PATTERN_BY_COUNTING`: Support any input pattern by counting high inputs rather than assuming a perfectly monotonic thermometer prefix.

The required trace names are: `time`, `th0`, `th1`, `th2`, `th3`, `th4`, `th5`, `th6`, `th7`, `b0`, `b1`, `b2`, `b3`.

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
