# Segmented DAC with DEM Control Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `segmented_dac_dem_top.va`: `segmented_dac_dem_top`
- `thermometer_decoder.va`: `thermometer_decoder`
- `binary_decoder.va`: `binary_decoder`
- `dwa_rotator.va`: `dwa_rotator`
- `dac_driver.va`: `dac_driver`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_DEM_RESET_CLEAR`: Reset clears vout, unit selection mask, and rotation pointer.
- `P_DEM_DAC_TRANSFER`: Each rising clock samples the unsigned 6-bit code and drives vref times code divided by 63.
- `P_DEM_ROTATED_MASK`: The selection mask contains the requested number of consecutive circular unit elements starting at the prior pointer.
- `P_DEM_POINTER_ADVANCE`: After each update the pointer advances by the requested unit count modulo eight.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `segmented_dac_dem_top.va`, `thermometer_decoder.va`, `binary_decoder.va`, `dwa_rotator.va`, `dac_driver.va`.
Every supplied `.va` file is editable; do not add or omit files.
