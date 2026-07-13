# Thermometer Bus Encoder

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `thermometer_bus_encoder.va`: `thermometer_bus_encoder`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_PREFIX_CODE`: Active segment outputs always form a contiguous prefix beginning at t0; no higher segment may be high while a lower segment is low.
- `P_ORDERED_ACTIVATION`: As vin increases, segments activate in order t0 through t15 and the active-segment count never decreases.
- `P_UNIFORM_SEGMENTS`: The clipped 0-to-vref input span selects among sixteen equal-width thermometer segments.
- `P_INPUT_CLIPPING`: Inputs at or below 0 V produce no active segments, and inputs at or above vref produce all sixteen active segments.
- `P_OUTPUT_LEVELS`: Each inactive segment approaches 0 V and each active segment approaches vh with finite transition smoothing.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `thermometer_bus_encoder.va`.
Do not add or omit artifacts.
