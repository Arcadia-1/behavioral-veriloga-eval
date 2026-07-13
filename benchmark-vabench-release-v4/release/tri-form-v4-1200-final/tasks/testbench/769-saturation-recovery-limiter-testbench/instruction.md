# Saturation Recovery Limiter Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Saturation Recovery Limiter` DUT. The evaluator runs the same submitted bytes
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

- `P_CLAMP_THE_ENABLED_INPUT_BETWEEN_THE`: Clamp the enabled input between the public low and high limiter levels.
- `P_DRIVE_A_SATURATION_FLAG_WHEN_EITHER`: Drive a saturation flag when either limiter boundary is active.
- `P_CLEAR_OUTPUT_FLAG_AND_RECOVERY_METRIC`: Clear output, flag, and recovery metric while enable is low.
- `P_COMPUTE_LIMITED_CLAMP_V_VIN_VLO`: Compute `limited = clamp(V(vin), vlo, vlimit)` while enabled and drive `out`
- `P_DRIVE_SAT_VHI_WHEN_ENABLED_AND`: Drive `sat = vhi` when enabled and `V(vin)` is outside `[vlo, vlimit]`;
- `P_DRIVE_THE_RECOVERY_METRIC_AS`: Drive the recovery metric as

The required trace names are: `time`, `vin`, `en`, `out`, `sat`, `recovery_metric`.

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
