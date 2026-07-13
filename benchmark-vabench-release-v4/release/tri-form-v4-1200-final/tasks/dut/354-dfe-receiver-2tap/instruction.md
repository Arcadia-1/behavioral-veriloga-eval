# 2-tap DFE Receiver

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `dfe_rx_top.va`: `dfe_rx_top`
- `slicer.va`: `slicer`
- `feedback_filter.va`: `feedback_filter`
- `decision_latch.va`: `decision_latch`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_CLEAR`: Reset clears the decision history and all public outputs.
- `P_TWO_TAP_FEEDBACK`: The feedback metric uses both configured taps and the previous two decisions.
- `P_CORRECTED_INPUT`: The debug slicer input equals VIN minus the active signed feedback correction.
- `P_CLOCKED_DECISION`: Each rising clock edge latches the threshold decision derived from the corrected input.
- `P_HISTORY_ORDER`: Feedback for a decision is based only on decisions from preceding clock edges.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `dfe_rx_top.va`, `slicer.va`, `feedback_filter.va`, `decision_latch.va`.
Do not add or omit artifacts.
