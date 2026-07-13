# Soft Hysteretic Limiter Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `soft_hysteretic_limiter.va`: `soft_hysteretic_limiter`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_NEUTRAL`: Initialization or active reset sets out and metric to 0.45 V and clears the remembered hysteresis offset.
- `P_HYSTERESIS_STATE_UPDATE`: On rising clk crossings, vin above 0.62 V stores +hys_step, vin below 0.38 V stores -hys_step, and vin within the middle band preserves the prior offset.
- `P_GAINED_LIMITER_TRANSFER`: The held output target is 0.45 V plus gain times vin minus 0.45 V plus the remembered hysteresis offset.
- `P_OUTPUT_LIMITS`: Out is clamped to 0.10 V through 0.82 V with finite transition smoothing.
- `P_STATE_METRIC`: Metric equals 0.45 V plus twice the remembered offset, producing 0.61 V and 0.29 V for the default high- and low-memory states.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `soft_hysteretic_limiter.va`.
Every supplied `.va` file is editable; do not add or omit files.
