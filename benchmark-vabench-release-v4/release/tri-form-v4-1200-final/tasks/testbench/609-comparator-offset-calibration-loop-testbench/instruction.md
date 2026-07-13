# Comparator Offset Calibration Loop Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Comparator Offset Calibration Loop` DUT. The evaluator runs the same submitted bytes
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

- `P_ZERO_INITIAL_ESTIMATE`: The signed estimate initializes to zero, the search increment initializes to step_initial, and valid begins low.
- `P_FALLING_EDGE_UPDATE`: The calibration state updates only on falling clk crossings through the midpoint of vdd and vss.
- `P_DECISION_DIRECTION`: At an update, a high dcmpp decreases the estimate by the current step and a low dcmpp increases it by the current step.
- `P_SUCCESSIVE_STEP_HALVING`: The magnitude of the search increment halves after every update, yielding a successive-approximation trajectory.
- `P_SYMMETRIC_DIFFERENTIAL_STIMULUS`: Vinp and vinn remain symmetric around mid-supply and vinp minus vinn equals offset_est.
- `P_VALID_COMPLETION`: Valid remains at vss until iterations updates complete, then rises to vdd and the reported estimate resolves the supplied comparator trip point represented by vos_ref within the search resolution.

The required trace names are: `time`, `vdd`, `vss`, `clk`, `dcmpp`, `vinp`, `vinn`, `offset_est`, `valid`, `vos_ref`.

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
