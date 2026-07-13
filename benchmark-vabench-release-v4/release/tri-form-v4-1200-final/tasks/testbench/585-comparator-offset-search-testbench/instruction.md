# Comparator Offset Search Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Comparator Offset Search` DUT. The evaluator runs the same submitted bytes
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

- `P_INITIAL_MEASUREMENT_STATE`: Before the first positive threshold crossing, valid, trip_v, and offset_est remain in the zero-measurement state.
- `P_DECISION_THRESHOLD`: Outp is high when V(inp,vss)-V(inn,vss) is above vos and low after that differential falls below vos.
- `P_FIRST_POSITIVE_CAPTURE`: The first positive crossing of the vos threshold captures the input trip voltage and measured differential offset and asserts valid.
- `P_CAPTURE_HOLD`: After valid asserts, trip_v, offset_est, and valid retain their first-measurement values despite later differential-input changes.
- `P_RAIL_REFERENCED_LOGIC`: Outp and valid use the vdd-to-vss logic range with finite transition smoothing.

The required trace names are: `time`, `vdd`, `vss`, `inp`, `inn`, `outp`, `trip_v`, `offset_est`, `valid`.

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
