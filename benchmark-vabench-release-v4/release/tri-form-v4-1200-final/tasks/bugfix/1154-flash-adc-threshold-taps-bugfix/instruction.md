# Flash ADC Threshold Taps Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `flash_adc_threshold_taps.va`: `flash_adc_threshold_taps`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_CLOCKED_SELECTED_THRESHOLD_TAPS`: Each rising `clk` crossing compares `vin` against the selected threshold taps and updates all thermometer outputs.
- `P_THERMOMETER_POLARITY`: Outputs assert high when `vin` exceeds their associated threshold and low otherwise.
- `P_OUTPUT_HIGH_LEVEL`: Asserted thermometer outputs use `vh` and inactive outputs use `vl`.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `flash_adc_threshold_taps.va`.
Every supplied `.va` file is editable; do not add or omit files.
