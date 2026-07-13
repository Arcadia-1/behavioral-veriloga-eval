# Reference Step Clock

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `ref_step_clk.va`: `ref_step_clk`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_SUPPLY_REFERENCED_RAILS`: CLK low and high levels track VSS and VDD respectively.
- `P_PRE_SWITCH_PERIOD`: Clock cycles before t_switch have full period period_pre.
- `P_POST_SWITCH_PERIOD`: Clock cycles scheduled after t_switch have full period period_post.
- `P_CADENCE_STEP`: The waveform changes cadence near t_switch without stopping, duplicating, or losing clock transitions.
- `P_HALF_DUTY_CYCLE`: CLK duty cycle remains close to 50 percent on both sides of the cadence step.
- `P_PARAMETERIZED_TIMING`: Nearby legal overrides of period_pre, period_post, t_switch, and tedge produce the corresponding periods, switch boundary, and edge smoothing.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `ref_step_clk.va`.
Do not add or omit artifacts.
