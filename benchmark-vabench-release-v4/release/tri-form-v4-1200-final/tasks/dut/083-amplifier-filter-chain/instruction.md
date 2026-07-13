# Amplifier Filter Chain

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `amplifier_filter_chain.va`: `amplifier_filter_chain`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_COMMON_MODE`: Initialization or active-high reset returns the preamp and both filter stages near 0.45 V and leaves settle_metric low.
- `P_BOUNDED_PREAMP`: At each rising clock edge, preamp_mon and metric equal gain times the sampled vin deviation about 0.45 V, clamped to 0 V through 0.9 V.
- `P_FIRST_FILTER_STAGE`: Filt1_mon applies the sampled first-order alpha update toward the bounded preamp target.
- `P_SECOND_FILTER_STAGE`: Filt2_mon applies a second sampled alpha update toward the newly updated first-stage value, and out follows filt2_mon.
- `P_CASCADE_LAG`: After a large input change, the second-stage output visibly lags the bounded preamp target while the two stage monitors preserve cascade order.
- `P_SETTLE_STATUS`: Settle_metric is 0.9 V when the output-target error is below 0.16 V and 0.1 V while the chain is recovering.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `amplifier_filter_chain.va`.
Do not add or omit artifacts.
