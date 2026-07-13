# 2-tap DFE Receiver Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `dfe_rx_top.va`: `dfe_rx_top`
- `slicer.va`: `slicer`
- `feedback_filter.va`: `feedback_filter`
- `decision_latch.va`: `decision_latch`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_CLEAR`: Reset clears the decision history and all public outputs.
- `P_TWO_TAP_FEEDBACK`: The feedback metric uses both configured taps and the previous two decisions.
- `P_CORRECTED_INPUT`: The debug slicer input equals VIN minus the active signed feedback correction.
- `P_CLOCKED_DECISION`: Each rising clock edge latches the threshold decision derived from the corrected input.
- `P_HISTORY_ORDER`: Feedback for a decision is based only on decisions from preceding clock edges.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `dfe_rx_top.va`, `slicer.va`, `feedback_filter.va`, `decision_latch.va`.
Every supplied `.va` file is editable; do not add or omit files.
