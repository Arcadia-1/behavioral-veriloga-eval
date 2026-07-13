# ADPLL Ratio Hop Timer

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `adpll_ratio_hop_ref.va`: `adpll_ratio_hop_ref`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RATIO_REQUEST_CLAMP`: The voltage-coded ratio request rounds V(ratio_ctrl) to the nearest integer with half-step boundaries and then clips the feedback divide ratio to the inclusive ratio_min through ratio_max range, including legal non-default override ranges.
- `P_DCO_FREQUENCY_BOUNDS`: The behavioral DCO on vout remains within the configured f_min and f_max limits.
- `P_FEEDBACK_DERIVED_FROM_DCO`: Feedback-clock activity is derived by dividing vout activity by the requested ratio rather than from an independent clock source.
- `P_BOUNDED_CONTROL_MONITOR`: Reference-versus-feedback timing error adjusts a bounded control state represented by rail-referenced vctrl_mon.
- `P_PRE_HOP_LOCK`: Stable pre-hop tracking produces lock only after lock_count_target consecutive feedback events satisfy lock_tol.
- `P_RATIO_HOP_REACQUISITION`: A changed ratio request causes loss of lock qualification followed by renewed lock after the loop tracks the new feedback cadence.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `adpll_ratio_hop_ref.va`.
Do not add or omit artifacts.
