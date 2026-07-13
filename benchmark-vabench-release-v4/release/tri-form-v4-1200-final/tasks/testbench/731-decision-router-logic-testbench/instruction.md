# Decision Router Logic Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Decision Router Logic` DUT. The evaluator runs the same submitted bytes
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

- `P_INTERPRET_VIN1_VIN2_AND_VALID_RELATIVE`: Interpret `vin1`, `vin2`, and `valid` relative to `vth`; all routed decisions below are evaluated from those voltage-coded Boolean inputs.
- `P_DRIVE_DM_HIGH_WHEN_VIN1_IS`: Drive `dm` high when `vin1` is high and low otherwise.
- `P_DRIVE_DL_HIGH_WHEN_VIN1_IS`: Drive `dl` high when `vin1` is low and `vin2` is high, and low otherwise.
- `P_DRIVE_X_HIGH_WHEN_VALID_IS`: Drive `x` high only when `valid` is high and both decision inputs are low.
- `P_DRIVE_Y_HIGH_WHEN_VALID_IS`: Drive `y` high only when `valid` is high and both decision inputs are high.
- `P_DRIVE_Z_HIGH_WHEN_VALID_IS`: Drive `z` high only when `valid` is high, `vin1` is low, and `vin2` is high.

The required trace names are: `time`, `vin1`, `vin2`, `valid`, `x`, `y`, `z`, `dm`, `dl`.

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
