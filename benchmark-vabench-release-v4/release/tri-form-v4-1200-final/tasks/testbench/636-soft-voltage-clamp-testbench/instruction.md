# Soft Voltage Clamp Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Soft Voltage Clamp` DUT. The evaluator runs the same submitted bytes
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

- `P_REFERENCED_INPUT_OUTPUT`: Use `V(vin, vgnd)` as input and drive `V(vout, vgnd)` as output.
- `P_LINEAR_MIDDLE_REGION`: Pass the input linearly for `0.0 V <= V(vin, vgnd) <= 0.4 V`.
- `P_SOFT_LOWER_LIMIT`: Below 0.0 V, apply an exponential soft lower limit that approaches -0.2 V with a 0.2 V softness span.
- `P_SOFT_UPPER_LIMIT`: Above 0.4 V, apply an exponential soft upper limit that approaches 0.6 V with a 0.2 V softness span.

The required trace names are: `time`, `vin`, `vout`.

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
