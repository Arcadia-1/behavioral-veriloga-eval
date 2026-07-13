# Acquisition Limited Sample And Hold

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `acquisition_limited_sample_hold.va`: `acquisition_limited_sample_hold`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET`: While rst is above vth, vout returns to vinit and metric is low.
- `P_ACQUISITION_ENABLE`: When sample is above vth and reset is inactive, metric is high and vout is allowed to acquire vin.
- `P_FINITE_ACQUISITION`: At each tick during acquisition, vout advances by alpha times the remaining difference from the current vin rather than jumping instantaneously.
- `P_ACQUISITION_CONVERGENCE`: For a constant vin and repeated acquisition updates, vout moves monotonically toward vin without overshoot for the declared alpha range.
- `P_HOLD`: A falling sample crossing freezes the last acquired value; vout holds it and metric remains low until acquisition resumes or reset is asserted.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `acquisition_limited_sample_hold.va`.
Do not add or omit artifacts.
