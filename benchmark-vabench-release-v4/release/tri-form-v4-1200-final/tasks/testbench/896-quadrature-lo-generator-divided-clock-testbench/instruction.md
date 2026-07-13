# Quadrature LO Generator from Divided Clock Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Quadrature LO Generator from Divided Clock` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_DISABLE_CLEAR`: Reset or disable clears both LO outputs, state metric, and quad_ok.
- `P_QUADRATURE_SEQUENCE`: Enabled rising input edges drive the repeating 10, 11, 01, 00 sequence.
- `P_DIVIDE_BY_FOUR`: Each LO has one cycle per four input rising edges with equal frequency and deterministic quadrature order.
- `P_STATE_METRIC`: div_metric reports the currently driven sequence index as k/3 of the output span.
- `P_QUAD_OK_DELAY`: quad_ok asserts only after two complete four-state output cycles.

The required trace names are: `time`, `clk_in`, `rst`, `enable`, `lo_i`, `lo_q`, `div_metric`, `quad_ok`.

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
