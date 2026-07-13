# Analog Mux Threshold Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Analog Mux Threshold` DUT. The evaluator runs the same submitted bytes
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

- `P_HIGH_SELECTS_VIN1`: When vsel is above vth, vout follows vin1 rather than vin2.
- `P_LOW_SELECTS_VIN2`: When vsel is at or below vth, vout follows vin2 rather than vin1.
- `P_BIDIRECTIONAL_SELECTION`: The selected input updates after both rising and falling crossings of vsel through vth.
- `P_INITIAL_SELECTION`: Before any select transition, vout is selected from the initial vsel level using the same strict-greater-than threshold rule.
- `P_NO_MIXING`: The output represents one selected input and does not average or sum vin1 and vin2.

The required trace names are: `time`, `vin1`, `vin2`, `vsel`, `vout`.

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
