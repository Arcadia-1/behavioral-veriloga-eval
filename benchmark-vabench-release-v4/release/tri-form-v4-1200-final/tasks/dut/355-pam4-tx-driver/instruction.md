# PAM4 Transmitter Driver

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `pam4_tx_top.va`: `pam4_tx_top`
- `gray_mapper.va`: `gray_mapper`
- `level_dac.va`: `level_dac`
- `preemphasis_driver.va`: `preemphasis_driver`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_CLEAR`: Reset clears mapped level, transition delta, and output drive.
- `P_GRAY_LEVEL_MAP`: The input bits map to levels 0, 1, 2, 3 in the declared Gray order.
- `P_LEVEL_DAC`: The mapped level selects the corresponding level-step voltage.
- `P_PREEMPHASIS`: Enabled pre-emphasis follows the sign of the symbol-to-symbol mapped-level transition.
- `P_OUTPUT_CLAMP`: The driven output remains between VSS and VDD.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `pam4_tx_top.va`, `gray_mapper.va`, `level_dac.va`, `preemphasis_driver.va`.
Do not add or omit artifacts.
