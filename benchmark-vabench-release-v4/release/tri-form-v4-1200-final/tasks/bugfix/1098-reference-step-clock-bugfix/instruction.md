# Reference Step Clock Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `ref_step_clk.va`: `ref_step_clk`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_SUPPLY_REFERENCED_RAILS`: CLK low and high levels track VSS and VDD respectively.
- `P_PRE_SWITCH_PERIOD`: Clock cycles before t_switch have full period period_pre.
- `P_POST_SWITCH_PERIOD`: Clock cycles scheduled after t_switch have full period period_post.
- `P_CADENCE_STEP`: The waveform changes cadence near t_switch without stopping, duplicating, or losing clock transitions.
- `P_HALF_DUTY_CYCLE`: CLK duty cycle remains close to 50 percent on both sides of the cadence step.
- `P_PARAMETERIZED_TIMING`: Nearby legal overrides of period_pre, period_post, t_switch, and tedge produce the corresponding periods, switch boundary, and edge smoothing.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `ref_step_clk.va`.
Every supplied `.va` file is editable; do not add or omit files.
