# Polyphase Quadrature Filter Macro

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `polyphase_quadrature_filter.va`: `polyphase_quadrature_filter`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_OR_WHEN_ENABLE_IS`: On reset or when `enable` is low, clear path states, metrics, `valid`, and drive outputs to `vcm`.
- `P_ON_EACH_RISING_CLK_EDGE_WHILE`: On each rising `clk` edge while enabled, update an in-phase sampled state from `vin`.
- `P_UPDATE_A_QUADRATURE_SAMPLED_STATE_USING`: Update a quadrature sampled state using the previous in-phase state so the Q output is phase-shifted relative to I.
- `P_DRIVE_I_OUT_AND_Q_OUT`: Drive `i_out` and `q_out` around `vcm` from the two path states.
- `P_REPORT_A_BOUNDED_PHASE_ORDER_METRIC`: Report a bounded phase/order metric on `phase_metric` and an amplitude-balance metric on `amp_metric`.
- `P_ASSERT_VALID_AFTER_AT_LEAST_FOUR`: Assert `valid` after at least four enabled sample updates.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `polyphase_quadrature_filter.va`.
Do not add or omit artifacts.
