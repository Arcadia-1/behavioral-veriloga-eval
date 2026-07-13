# Offset Bisection Driver Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Offset Bisection Driver` DUT. The evaluator runs the same submitted bytes
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

- `P_BISECTION_INITIAL_STATE`: The differential residue initializes to zero, the step initializes to `step_initial`, and the previous decision polarity initializes to the low-decision direction.
- `P_FALLING_CLOCK_DECISION_UPDATE`: On each falling `clk` crossing, sample `vout` and update the residue using the specified comparator polarity.
- `P_SIGN_CHANGE_STEP_HALVING`: The bisection step halves when the sampled decision polarity changes.
- `P_VCM_CENTERED_DIFFERENTIAL_DRIVE`: `vinp` and `vinn` remain centered around `vcm` with half of the differential residue on each side.

The required trace names are: `time`, `clk`, `vout`, `vcm`, `vinp`, `vinn`.

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
