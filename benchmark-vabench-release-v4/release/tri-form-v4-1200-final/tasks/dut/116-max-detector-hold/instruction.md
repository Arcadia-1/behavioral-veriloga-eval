# Max Detector Hold

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `max_detector_hold.va`: `max_detector_hold`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_INITIAL_INPUT`: At simulation start, the held output is initialized from the input rather than from a fixed rail.
- `P_CAPTURE_NEW_MAX`: Whenever vin exceeds every previously observed value, vout updates to that new maximum.
- `P_HOLD_ON_FALL`: When vin falls below the held maximum, vout retains the previously captured maximum.
- `P_MONOTONE_OUTPUT`: Across transient operation, vout is monotone nondecreasing.
- `P_RUNNING_MAX`: At each observation time, vout equals the maximum vin value observed from simulation start through that time.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `max_detector_hold.va`.
Do not add or omit artifacts.
