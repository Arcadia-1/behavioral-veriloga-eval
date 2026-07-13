# CPPLL Tracking Reacquire Timer

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `cppll_timer_ref.va`: `cppll_timer_ref`
- `ref_step_clk.va`: `ref_step_clk`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_REFERENCE_PERIOD_STEP`: The bundled reference-step clock produces the configured period_pre cadence before t_switch and period_post cadence afterwards, with rail-referenced levels.
- `P_DCO_FREQUENCY_CONTROL`: Dco_clk frequency responds to bounded vctrl_mon around f_center with kvco_hz_per_v sensitivity and remains clamped to f_min through f_max.
- `P_FEEDBACK_DIVISION`: Fb_clk is derived from dco_clk rising-edge activity using div_ratio.
- `P_BOUNDED_TRACKING_CONTROL`: Reference-versus-feedback phase error updates proportional and bounded integral correction while vctrl_mon remains within the supply rails.
- `P_INITIAL_LOCK_ACQUISITION`: Stable pre-step tracking asserts lock only after lock_count_target consecutive in-tolerance events.
- `P_DISTURBANCE_UNLOCK`: The reference-period step removes or destabilizes lock qualification while the loop responds to the changed cadence.
- `P_LATE_REACQUISITION`: After the step, fb_clk tracks the new reference cadence and lock reasserts while vctrl_mon remains rail-bounded.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `cppll_timer_ref.va`, `ref_step_clk.va`.
Do not add or omit artifacts.
