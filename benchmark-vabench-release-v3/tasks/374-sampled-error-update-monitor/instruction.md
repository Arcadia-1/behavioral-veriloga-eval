# Sampled Error Update Monitor

Implement one Verilog-A source file named `sampled_error_update_monitor.va`.

## Task Contract

Build a Spectre-compatible voltage-domain behavioral DUT source for a clocked
calibration helper that updates a corrected value and its error/progress
metrics. Implement only the `sampled_error_update_monitor` module.

## Public Verilog-A Interface

```verilog
module sampled_error_update_monitor(clk, rst, sample, target, coef, out, err_metric, progress);
```

All ports are electrical. `clk` is the sampling clock, `rst` is an active-high
reset, `sample`, `target`, and `coef` are voltage-coded inputs, and `out`,
`err_metric`, and `progress` are voltage-coded observables.

## Public Parameter Contract

- `parameter real vth = 0.45`.
- `parameter real vhi = 0.9`.
- `parameter real err_fullscale = 0.50`.
- `parameter real err_window = 0.040`.
- `parameter integer ready_count = 3`.
- `parameter real tr = 60p`.

## Required Behavior

Initialize the stable-count state and all observables to zero. On each rising
clock crossing, clear the stable count, `out`, `err_metric`, and `progress`
while `rst` is high. Otherwise compute `coeff = clip01(V(coef) / vhi)`,
`err = V(target) - V(sample)`, and
`corrected = V(sample) + coeff * err`. Drive `out` as `corrected` clamped into
`[0, vhi]`, and drive `err_metric = vhi * clip01(abs(err) / err_fullscale)`.

If `abs(err) <= err_window`, increment the stable count by one up to
`ready_count`; otherwise clear the stable count. Drive
`progress = vhi * clip01(stable_count / ready_count)`. Hold the last observable
values between rising clock crossings.

## Modeling Constraints

Use voltage-domain behavioral Verilog-A only. Use local analog helper functions
rather than user `task`/`endtask` syntax. Do not use Verilog-AMS digital
kernels, branch current contributions, transistor devices, `ddt()`, or
`idt()`. Do not hard-code testbench stimulus times.

## Output Contract

Return only `sampled_error_update_monitor.va` implementing the public module. The file must compile under Spectre-compatible Verilog-A and must not require additional modules, include files beyond standard disciplines, or testbench changes.
