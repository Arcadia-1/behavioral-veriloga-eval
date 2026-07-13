# Dual Track Sample Hold Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Dual Track Sample Hold` DUT. The evaluator runs the same submitted bytes
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

- `P_COMPLEMENTARY_TRACK_HOLD_SEQUENCE`: During low clock phase the input stage tracks `vin` while output holds; after the rising edge, the output stage tracks the retained input-stage value during high clock phase; after the falling edge, output holds until the next high phase.
- `P_FINITE_TRACKING_AND_HOLD`: Use finite acquisition updates and preserve held values between tracking windows rather than making the output continuously transparent or a single ideal edge sample.
- `P_PHASE_MONITOR_POLARITY`: Drive `phase` high only during output-stage tracking and low otherwise.

The required trace names are: `time`, `vin`, `clk`, `vout`, `phase`, `vdd`, `vss`.

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
