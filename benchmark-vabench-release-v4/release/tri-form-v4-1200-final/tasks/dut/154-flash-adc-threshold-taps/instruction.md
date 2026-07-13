# Flash ADC Threshold Taps

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `flash_adc_threshold_taps.va`: `flash_adc_threshold_taps`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_CLOCKED_SELECTED_THRESHOLD_TAPS`: Each rising `clk` crossing compares `vin` against the selected threshold taps and updates all thermometer outputs.
- `P_THERMOMETER_POLARITY`: Outputs assert high when `vin` exceeds their associated threshold and low otherwise.
- `P_OUTPUT_HIGH_LEVEL`: Asserted thermometer outputs use `vh` and inactive outputs use `vl`.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `flash_adc_threshold_taps.va`.
Do not add or omit artifacts.
