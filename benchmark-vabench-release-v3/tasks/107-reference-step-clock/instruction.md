# Reference Step Clock

Implement `ref_step_clk.va` in Verilog-A.

## Public Interface

Declare module `ref_step_clk(VDD, VSS, CLK)` with scalar electrical
voltage-domain ports. `VDD` and `VSS` are supply rails and `CLK` is a
voltage-coded clock output.

## Public Parameter Contract

- `period_pre`: output clock period before the frequency step, default `20n`.
- `period_post`: output clock period after the frequency step, default `19.5n`.
- `t_switch`: time at which subsequent half-period scheduling uses
  `period_post`, default `2u`.
- `tedge`: output transition smoothing time, default `100p`.

## Functional Contract

- Initialize `CLK` low and schedule the first toggle after half of
  `period_pre`.
- Toggle `CLK` on timer events.
- Before `t_switch`, schedule toggles using `period_pre / 2`.
- At and after `t_switch`, schedule toggles using `period_post / 2`.
- Drive `CLK` rail-to-rail relative to `VDD` and `VSS` with smoothed
  transitions.

## Modeling Constraints

Return only `ref_step_clk.va`; companion files used by the validation scenario
are supplied separately. Do not emit a Spectre testbench, checker logic,
private test hooks, or simulator-private side channels. Use voltage-domain,
event-driven Verilog-A; do not use transistor-level devices, current
contributions, `ddt()`, or `idt()`.
