# Two Bit Counter Marker Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Two Bit Counter Marker` DUT. The evaluator runs the same submitted bytes
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

- `P_INITIAL_LOW`: The timing/readout marker output initializes at 0.0 V before any counted edge.
- `P_RISING_EDGE_COUNT`: Only rising crossings of CLKIN through 0.5 V advance the internal modulo-four sequence.
- `P_WRAP_MARKER`: MC is driven to the 1.0 V marker level on the counted edge that wraps the sequence from count 3 to count 0.
- `P_NONWRAP_LOW`: MC is driven to 0.0 V on each of the other three counted edges in every four-edge cycle.
- `P_PERIOD_FOUR`: For a continuing valid clock, marker assertions repeat once per four rising threshold crossings.

The required trace names are: `time`, `clkin`, `mc`.

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
