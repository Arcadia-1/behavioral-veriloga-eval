# Offset Halving Search Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Offset Halving Search` DUT. The evaluator runs the same submitted bytes
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

- `P_INITIALIZE_THE_DIFFERENTIAL_TRIM_RESIDUE_TO`: Initialize the differential trim residue to zero and the active step to `step_initial`. On each falling `clk` crossing before lockout, sample `dcmpp`: a high decision moves the differential trim negative and a low decision moves it positive. Clamp the signed residue to `+/-diff_limit`. Halve the active step after each update; once the next step would be below `step_min`, lock the trim code and hold the existing residue for later clock edges. Drive `vinp` and `vinn` symmetrically around `0.5*vdd` from the current residue.

The required trace names are: `time`, `clk`, `dcmpp`, `vinp`, `vinn`.

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
