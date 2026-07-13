# Three Way Threshold Mux Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Three Way Threshold Mux` DUT. The evaluator runs the same submitted bytes
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

- `P_DIFFERENTIAL_CONTROL`: Use `V(cntrlp, cntrlm)` as the mux control signal.
- `P_LOW_REGION_SELECTS_SIGIN1`: When control is below `sigth_low`, drive `sigout` from `sigin1`.
- `P_MIDDLE_REGION_SELECTS_SIGIN2`: When control is in the inclusive window `[sigth_low, sigth_high]`, drive `sigout` from `sigin2`.
- `P_HIGH_REGION_SELECTS_SIGIN3`: When control is above `sigth_high`, drive `sigout` from `sigin3`.

The required trace names are: `time`, `cntrlm`, `cntrlp`, `sigin1`, `sigin2`, `sigin3`, `sigout`.

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
