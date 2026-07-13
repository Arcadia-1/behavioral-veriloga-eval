# Strongarm Style Latch Comparator Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Strongarm Style Latch Comparator` DUT. The evaluator runs the same submitted bytes
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

- `P_INITIAL_AND_FALLING_RESET`: All decision and latch monitor outputs initialize low and return low after each falling clock crossing.
- `P_POSITIVE_DECISION`: A rising clock crossing with VINP minus VINN minus voffset positive latches DCMPP and LP high while DCMPN and LM remain low.
- `P_NEGATIVE_DECISION`: A rising clock crossing with VINP minus VINN minus voffset negative latches DCMPN and LM high while DCMPP and LP remain low.
- `P_ZERO_DIFFERENTIAL`: An exactly zero effective differential sampled at a rising clock crossing leaves both complementary decision states low.
- `P_LATCH_HOLD`: The sampled decision is held between clock events and does not track input changes while the clock remains high.

The required trace names are: `time`, `clk`, `vinp`, `vinn`, `out_p`, `out_n`, `lp`, `lm`, `vss`, `vdd`.

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
