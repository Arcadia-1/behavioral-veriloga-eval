# Phase Detector Chopper

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `phase_detector_chopper.va`: `phase_detector_chopper`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_POSITIVE_LO_GAIN_PATH`: When `vlocal_osc` is positive, drive `vif = gain * vin_rf`.
- `P_NEGATIVE_LO_CHOP_PATH`: When `vlocal_osc` is not positive, drive `vif = -gain * vin_rf`.
- `P_CONTINUOUS_TRACKING`: `vif` tracks `vin_rf` and `vlocal_osc` continuously without clocked state or hidden latching.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `phase_detector_chopper.va`.
Do not add or omit artifacts.
