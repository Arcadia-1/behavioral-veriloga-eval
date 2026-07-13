# Segmented DAC

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `segmented_dac.va`: `segmented_dac`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_SEGMENT_WEIGHTS`: b0 and b1 contribute one and two LSB steps while each active thermometer control contributes four LSB steps.
- `P_CODE_MONOTONICITY`: Increasing the summed segmented code does not decrease aout.
- `P_ENDPOINTS`: The zero code maps to vss and the all-active 15-step code maps to vref.
- `P_RAIL_RELATIVE_MAPPING`: Intermediate codes linearly span the vss-to-vref range.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `segmented_dac.va`.
Do not add or omit artifacts.
