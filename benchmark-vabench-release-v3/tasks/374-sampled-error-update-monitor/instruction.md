# Sampled Error Update Monitor

Implement one Verilog-A source file named `sampled_error_update_monitor.va`.

## Task Contract

Build a Spectre-compatible voltage-domain behavioral model for Clocked calibration helper that updates a corrected value and its error/progress metrics.

## Form-Specific Requirements

This is a DUT source task. Implement only the `sampled_error_update_monitor` module; no external testbench, checker logic, transistor devices, or extra helper module is part of the requested artifact.

## Public Verilog-A Interface

```verilog
module sampled_error_update_monitor(clk, rst, sample, target, coef, out, err_metric, progress);
```

## Public Parameter Contract

- `parameter real vth = 0.45`.
- `parameter real vhi = 0.9`.
- `parameter real err_fullscale = 0.50`.
- `parameter real err_window = 0.040`.
- `parameter integer ready_count = 3`.
- `parameter real tr = 60p`.

## Required Behavior

- On each rising clock crossing, blend sample toward target using the public coefficient voltage.
- Drive the corrected output and an absolute error metric as correlated outputs.
- Accumulate progress only after consecutive in-window sampled errors.
- Clear all sampled state while reset is high.
- Use local analog helper functions rather than user task/endtask syntax.

## Modeling Constraints

Use voltage-domain behavioral Verilog-A only. Do not use user `task`/`endtask`, Verilog-AMS digital kernels, branch current contributions, transistor devices, `ddt()`, or `idt()`. Do not hard-code visible or hidden stimulus times.

## Output Contract

Return only `sampled_error_update_monitor.va` implementing the public module. The file must compile under Spectre-compatible Verilog-A and must not require additional modules, include files beyond standard disciplines, or testbench changes.
