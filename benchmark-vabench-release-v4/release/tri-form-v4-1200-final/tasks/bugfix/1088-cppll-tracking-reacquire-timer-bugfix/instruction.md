# CPPLL Tracking Reacquire Timer Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `cppll_timer_ref.va`: `cppll_timer_ref`
- `ref_step_clk.va`: `ref_step_clk`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_REFERENCE_PERIOD_STEP`: The bundled reference-step clock produces the configured period_pre cadence before t_switch and period_post cadence afterwards, with rail-referenced levels.
- `P_DCO_FREQUENCY_CONTROL`: Dco_clk frequency responds to bounded vctrl_mon around f_center with kvco_hz_per_v sensitivity and remains clamped to f_min through f_max.
- `P_FEEDBACK_DIVISION`: Fb_clk is derived from dco_clk rising-edge activity using div_ratio.
- `P_BOUNDED_TRACKING_CONTROL`: Reference-versus-feedback phase error updates proportional and bounded integral correction while vctrl_mon remains within the supply rails.
- `P_INITIAL_LOCK_ACQUISITION`: Stable pre-step tracking asserts lock only after lock_count_target consecutive in-tolerance events.
- `P_DISTURBANCE_UNLOCK`: The reference-period step removes or destabilizes lock qualification while the loop responds to the changed cadence.
- `P_LATE_REACQUISITION`: After the step, fb_clk tracks the new reference cadence and lock reasserts while vctrl_mon remains rail-bounded.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `cppll_timer_ref.va`, `ref_step_clk.va`.
Every supplied `.va` file is editable; do not add or omit files.
