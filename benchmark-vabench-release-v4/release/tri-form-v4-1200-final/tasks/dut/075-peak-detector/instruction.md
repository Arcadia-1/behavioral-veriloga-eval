# Peak Detector

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `peak_detector.va`: `peak_detector`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_INITIAL_ZERO`: The retained peak and vout initialize to 0 V.
- `P_SAMPLED_MEASUREMENT`: When reset is inactive, vin is considered for peak updates at periodic 500 ps sample instants.
- `P_MAX_RETENTION`: At each sample, a vin value above the retained peak replaces it; lower or equal samples leave vout unchanged.
- `P_MONOTONIC_HOLD`: Between resets, the retained peak does not decrease and remains held between sample instants.
- `P_RESET_CLEAR`: While rst is above vth, the retained peak is cleared and vout returns to 0 V.
- `P_OUTPUT_SMOOTHING`: Changes of the retained peak appear on vout with finite transition smoothing set by tr.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `peak_detector.va`.
Do not add or omit artifacts.
