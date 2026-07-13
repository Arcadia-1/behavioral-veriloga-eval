# Acquisition Limited Sample And Hold Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Acquisition Limited Sample And Hold` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET`: While rst is above vth, vout returns to vinit and metric is low.
- `P_ACQUISITION_ENABLE`: When sample is above vth and reset is inactive, metric is high and vout is allowed to acquire vin.
- `P_FINITE_ACQUISITION`: At each tick during acquisition, vout advances by alpha times the remaining difference from the current vin rather than jumping instantaneously.
- `P_ACQUISITION_CONVERGENCE`: For a constant vin and repeated acquisition updates, vout moves monotonically toward vin without overshoot for the declared alpha range.
- `P_HOLD`: A falling sample crossing freezes the last acquired value; vout holds it and metric remains low until acquisition resumes or reset is asserted.

The required trace names are: `time`, `sample`, `rst`, `vin`, `vout`, `metric`.

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
