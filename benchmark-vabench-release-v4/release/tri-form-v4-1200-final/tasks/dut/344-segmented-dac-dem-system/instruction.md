# Segmented DAC with DEM Control

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `segmented_dac_dem_top.va`: `segmented_dac_dem_top`
- `thermometer_decoder.va`: `thermometer_decoder`
- `binary_decoder.va`: `binary_decoder`
- `dwa_rotator.va`: `dwa_rotator`
- `dac_driver.va`: `dac_driver`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_DEM_RESET_CLEAR`: Reset clears vout, unit selection mask, and rotation pointer.
- `P_DEM_DAC_TRANSFER`: Each rising clock samples the unsigned 6-bit code and drives vref times code divided by 63.
- `P_DEM_ROTATED_MASK`: The selection mask contains the requested number of consecutive circular unit elements starting at the prior pointer.
- `P_DEM_POINTER_ADVANCE`: After each update the pointer advances by the requested unit count modulo eight.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `segmented_dac_dem_top.va`, `thermometer_decoder.va`, `binary_decoder.va`, `dwa_rotator.va`, `dac_driver.va`.
Do not add or omit artifacts.
