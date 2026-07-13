# SAR Weighted Sum

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `sar_weighted_sum.va`: `sar_weighted_sum`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_THRESHOLD_DECODE`: Each D input contributes logic 1 only while its voltage is strictly above vth; a value at or below vth contributes logic 0.
- `P_WEIGHT_ORDER`: The decoded contribution order is D10 at seven-eighths full scale, D9 at one-half, D8 at one-quarter, a 5:3 split across D7 and D6, then a binary tail from D5 through D0.
- `P_BIPOLAR_ENDPOINTS`: All decision inputs low produce -1 V, while all decision inputs high produce one 512-unit step below +1 V on the normalized bipolar scale.
- `P_MONOTONIC_CODE_WEIGHT`: Changing any decoded decision from low to high without lowering another decision cannot decrease VOUT.
- `P_CONTINUOUS_DECODE`: VOUT continuously reflects the current threshold-decoded input combination without a clock, reset, or retained code state.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `sar_weighted_sum.va`.
Do not add or omit artifacts.
