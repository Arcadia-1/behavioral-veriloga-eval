# Limiting Differential Amplifier

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `limiting_differential_amplifier.va`: `limiting_differential_amplifier`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_OFFSET_CORRECTED_DIFFERENTIAL_GAIN`: Compute `gain * (V(sigin_p, sigin_n) - sigin_offset)`.
- `P_OUTPUT_MIDPOINT_REFERENCE`: Center the amplified value at `(sigout_high + sigout_low) / 2`.
- `P_OUTPUT_RAIL_CLAMP`: Clamp the final target to the inclusive interval `[sigout_low, sigout_high]`.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `limiting_differential_amplifier.va`.
Do not add or omit artifacts.
