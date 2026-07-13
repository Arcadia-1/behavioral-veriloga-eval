# Control Word Encoder 7b Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Control Word Encoder 7b` DUT. The evaluator runs the same submitted bytes
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

- `P_SEVEN_BIT_DECODE`: `ctrl` is decoded LSB-first so `d0` carries bit 0 and `d6` carries bit 6.
- `P_BIT_POLARITY`: A decoded one drives its output high and a decoded zero drives its output low.
- `P_OUTPUT_RAIL_LEVELS`: Each output uses the declared `vhi` and `vlo` voltage levels for its decoded bit.

The required trace names are: `time`, `d0_0`, `d1_0`, `d2_0`, `d3_0`, `d4_0`, `d5_0`, `d6_0`, `d0_19`, `d1_19`, `d2_19`, `d3_19`, `d4_19`, `d5_19`, `d6_19`, `d0_108`, `d1_108`, `d2_108`, `d3_108`, `d4_108`, `d5_108`, `d6_108`, `d0_127`, `d1_127`, `d2_127`, `d3_127`, `d4_127`, `d5_127`, `d6_127`.

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
