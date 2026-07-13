# Start Gated Offset Search

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `start_gated_offset_search.va`: `start_gated_offset_search`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_DISABLED_COMMON_MODE`: While START is below vstart_th, VINP and VINN both equal vcm and the internal search state is reset.
- `P_START_REINITIALIZATION`: Each rising START crossing through vstart_th reinitializes differential value to zero, step to 20 mV, and remembered direction high.
- `P_FALLING_CLOCK_UPDATES`: While START is high, search updates occur only on falling CLK crossings through vdd/2.
- `P_DECISION_DIRECTED_STEP`: At each enabled update, VOUT above vdd/2 moves the differential value positive and VOUT at or below vdd/2 moves it negative.
- `P_REVERSAL_STEP_HALVING`: When the newly sampled decision direction differs from the remembered direction, the current step is halved before applying the move.
- `P_COMMON_MODE_AND_DIFFERENTIAL`: During search, the average of VINP and VINN remains vcm and their difference equals the accumulated differential search value.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `start_gated_offset_search.va`.
Do not add or omit artifacts.
