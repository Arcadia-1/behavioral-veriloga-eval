# Calibration Deadband Controller Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Calibration Deadband Controller` DUT. The evaluator runs the same submitted bytes
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

- `P_INITIAL_AND_RESET_TARGET`: Out initializes to target and returns to target while rst is above vth; metric is low during reset.
- `P_POSITIVE_ERROR_STEP`: At a rising clock crossing with vin minus target greater than deadband, out increases by one step_size and metric goes high.
- `P_NEGATIVE_ERROR_STEP`: At a rising clock crossing with vin minus target less than negative deadband, out decreases by one step_size and metric goes high.
- `P_DEADBAND_HOLD`: At a rising clock crossing with signed error inside the inclusive deadband, out holds and metric remains low.
- `P_OUTPUT_CLAMP`: Repeated updates cannot drive out below vmin or above vmax.
- `P_BETWEEN_EDGE_HOLD`: Out state does not follow vin between rising clock crossings.

The required trace names are: `time`, `clk`, `rst`, `vin`, `out`, `metric`.

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
