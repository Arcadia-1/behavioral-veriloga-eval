# Saturation Recovery Limiter

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `saturation_recovery_limiter.va`: `saturation_recovery_limiter`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_CLAMP_THE_ENABLED_INPUT_BETWEEN_THE`: Clamp the enabled input between the public low and high limiter levels.
- `P_DRIVE_A_SATURATION_FLAG_WHEN_EITHER`: Drive a saturation flag when either limiter boundary is active.
- `P_CLEAR_OUTPUT_FLAG_AND_RECOVERY_METRIC`: Clear output, flag, and recovery metric while enable is low.
- `P_COMPUTE_LIMITED_CLAMP_V_VIN_VLO`: Compute `limited = clamp(V(vin), vlo, vlimit)` while enabled and drive `out`
- `P_DRIVE_SAT_VHI_WHEN_ENABLED_AND`: Drive `sat = vhi` when enabled and `V(vin)` is outside `[vlo, vlimit]`;
- `P_DRIVE_THE_RECOVERY_METRIC_AS`: Drive the recovery metric as

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `saturation_recovery_limiter.va`.
Do not add or omit artifacts.
