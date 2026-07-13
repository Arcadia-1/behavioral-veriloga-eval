# Fractional-N Divider Accumulator Flow

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `fracn_pll_timer_ref.va`: `fracn_pll_timer_ref`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_USE_REF_CLK_AS_THE_REFERENCE`: Use `ref_clk` as the reference timing input.
- `P_GENERATE_A_BEHAVIORAL_DCO_CLOCK_ON`: Generate a behavioral DCO clock on `dco_clk`.
- `P_GENERATE_FB_CLK_BY_TOGGLING_IT`: Generate `fb_clk` by toggling it after a DCO rising-edge count selected by a
- `P_UPDATE_A_BOUNDED_CONTROL_VOLTAGE_MONITOR`: Update a bounded control-voltage monitor on `vctrl_mon` from the PFD phase
- `P_DRIVE_LOCK_HIGH_AFTER_STABLE_TRACKING`: Drive `lock` high after stable tracking, low or unstable during the

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `fracn_pll_timer_ref.va`.
Do not add or omit artifacts.
