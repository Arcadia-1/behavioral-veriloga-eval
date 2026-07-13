# SAR Weighted Sum Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `sar_weighted_sum.va`: `sar_weighted_sum`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_THRESHOLD_DECODE`: Each D input contributes logic 1 only while its voltage is strictly above vth; a value at or below vth contributes logic 0.
- `P_WEIGHT_ORDER`: The decoded contribution order is D10 at seven-eighths full scale, D9 at one-half, D8 at one-quarter, a 5:3 split across D7 and D6, then a binary tail from D5 through D0.
- `P_BIPOLAR_ENDPOINTS`: All decision inputs low produce -1 V, while all decision inputs high produce one 512-unit step below +1 V on the normalized bipolar scale.
- `P_MONOTONIC_CODE_WEIGHT`: Changing any decoded decision from low to high without lowering another decision cannot decrease VOUT.
- `P_CONTINUOUS_DECODE`: VOUT continuously reflects the current threshold-decoded input combination without a clock, reset, or retained code state.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `sar_weighted_sum.va`.
Every supplied `.va` file is editable; do not add or omit files.
