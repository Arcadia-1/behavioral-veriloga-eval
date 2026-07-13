# Divide By Eight Clock

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `divide_by_eight_clock.va`: `divide_by_eight_clock`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_FORCES_INITIAL_HIGH`: Active-high `rst` forces the divider counter to zero and drives `vout` high regardless of input-clock activity.
- `P_ENABLE_QUALIFIED_DIVIDE_BY_EIGHT`: Rising `vin` crossings through `vth` advance the divide-by-eight counter only while `en` is high.
- `P_OUTPUT_DUTY_AND_LEVEL`: The divided waveform follows the specified high/low count window and uses the declared high and low voltage levels.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `divide_by_eight_clock.va`.
Do not add or omit artifacts.
