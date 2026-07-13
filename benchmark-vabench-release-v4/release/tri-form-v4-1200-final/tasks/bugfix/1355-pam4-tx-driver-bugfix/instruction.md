# PAM4 Transmitter Driver Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `pam4_tx_top.va`: `pam4_tx_top`
- `gray_mapper.va`: `gray_mapper`
- `level_dac.va`: `level_dac`
- `preemphasis_driver.va`: `preemphasis_driver`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_CLEAR`: Reset clears mapped level, transition delta, and output drive.
- `P_GRAY_LEVEL_MAP`: The input bits map to levels 0, 1, 2, 3 in the declared Gray order.
- `P_LEVEL_DAC`: The mapped level selects the corresponding level-step voltage.
- `P_PREEMPHASIS`: Enabled pre-emphasis follows the sign of the symbol-to-symbol mapped-level transition.
- `P_OUTPUT_CLAMP`: The driven output remains between VSS and VDD.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `pam4_tx_top.va`, `gray_mapper.va`, `level_dac.va`, `preemphasis_driver.va`.
Every supplied `.va` file is editable; do not add or omit files.
