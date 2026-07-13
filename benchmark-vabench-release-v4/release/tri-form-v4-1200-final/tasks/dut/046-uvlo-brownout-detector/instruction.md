# UVLO Brownout Detector

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `uvlo_brownout_detector.va`: `uvlo_brownout_detector`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_FAULT`: Active reset clears the power-good out signal and drives metric to the public fault code 0.9 V.
- `P_UPPER_TRIP_ASSERT`: On a sampled update, vin strictly greater than 0.65 V asserts power-good out.
- `P_HYSTERESIS_HOLD`: For sampled vin values from 0.55 V through 0.65 V inclusive, out preserves its previous power-good state.
- `P_BROWNOUT_CLEAR`: On a sampled update, vin strictly less than 0.55 V clears out to the brownout state.
- `P_STATUS_DISTINCTION`: Metric is the checker-observable status code: 0.1 V when out is power-good high and 0.9 V when reset, undervoltage, or brownout is active.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `uvlo_brownout_detector.va`.
Do not add or omit artifacts.
