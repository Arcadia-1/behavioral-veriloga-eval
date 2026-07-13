# DAC Mismatch Unit Weighting Model Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `DAC Mismatch Unit Weighting Model` DUT. The evaluator runs the same submitted bytes
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

- `P_ZERO_AND_FULL_SCALE`: All-zero input maps to vlo and all-active input maps to vhi after transition settling.
- `P_NONIDEAL_WEIGHT_SUM`: Inputs b0 through b3 contribute fixed positive weights 1.00, 2.02, 3.96, and 8.08 normalized by their all-active sum.
- `P_LOGIC_THRESHOLD`: Each bit is independently interpreted using the public fixed 0.45 V decision threshold.
- `P_BOUNDED_OUTPUT`: For every input pattern, the settled output remains within the vlo-to-vhi interval.
- `P_MISMATCH_OBSERVABILITY`: Single-bit output increments preserve the stated nonideal weighting rather than ideal powers-of-two weighting.

The required trace names are: `time`, `b0`, `b1`, `b2`, `b3`, `out`.

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
