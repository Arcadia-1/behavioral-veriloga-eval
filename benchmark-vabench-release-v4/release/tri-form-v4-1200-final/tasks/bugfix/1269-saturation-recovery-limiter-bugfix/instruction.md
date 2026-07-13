# Saturation Recovery Limiter Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `saturation_recovery_limiter.va`: `saturation_recovery_limiter`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_CLAMP_THE_ENABLED_INPUT_BETWEEN_THE`: Clamp the enabled input between the public low and high limiter levels.
- `P_DRIVE_A_SATURATION_FLAG_WHEN_EITHER`: Drive a saturation flag when either limiter boundary is active.
- `P_CLEAR_OUTPUT_FLAG_AND_RECOVERY_METRIC`: Clear output, flag, and recovery metric while enable is low.
- `P_COMPUTE_LIMITED_CLAMP_V_VIN_VLO`: Compute `limited = clamp(V(vin), vlo, vlimit)` while enabled and drive `out`
- `P_DRIVE_SAT_VHI_WHEN_ENABLED_AND`: Drive `sat = vhi` when enabled and `V(vin)` is outside `[vlo, vlimit]`;
- `P_DRIVE_THE_RECOVERY_METRIC_AS`: Drive the recovery metric as

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `saturation_recovery_limiter.va`.
Every supplied `.va` file is editable; do not add or omit files.
