# 2-tap DFE Receiver Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `2-tap DFE Receiver` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_CLEAR`: Reset clears the decision history and all public outputs.
- `P_TWO_TAP_FEEDBACK`: The feedback metric uses both configured taps and the previous two decisions.
- `P_CORRECTED_INPUT`: The debug slicer input equals VIN minus the active signed feedback correction.
- `P_CLOCKED_DECISION`: Each rising clock edge latches the threshold decision derived from the corrected input.
- `P_HISTORY_ORDER`: Feedback for a decision is based only on decisions from preceding clock edges.

The required trace names are: `time`, `vin`, `clk`, `rst`, `tap1_1`, `tap1_0`, `tap2_1`, `tap2_0`, `decision`, `fb_metric`, `slicer_in_dbg`.

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
