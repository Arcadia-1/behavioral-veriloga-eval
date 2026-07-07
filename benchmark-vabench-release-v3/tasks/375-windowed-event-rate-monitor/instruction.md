# Windowed Event Rate Monitor

Implement one Verilog-A source file named `windowed_event_rate_monitor.va`.

## Task Contract

Build a Spectre-compatible voltage-domain behavioral model for Clocked measurement helper that reports event rate and observed average over a qualified window.

## Form-Specific Requirements

This is a DUT source task. Implement only the `windowed_event_rate_monitor` module; no external testbench, checker logic, transistor devices, or extra helper module is part of the requested artifact.

## Public Verilog-A Interface

```verilog
module windowed_event_rate_monitor(clk, rst, event_in, gate, rate, average);
```

## Public Parameter Contract

- `parameter real vth = 0.45`.
- `parameter real vhi = 0.9`.
- `parameter integer window_count = 5`.
- `parameter real tr = 60p`.

## Required Behavior

- Sample event_in on rising clock crossings only while gate is high and reset is low.
- Clear the measurement window on reset or gate-low samples.
- Drive rate as a clipped count/window metric.
- Drive average as count divided by sampled gated updates.
- Use local analog helper functions rather than user task/endtask syntax.

## Modeling Constraints

Use voltage-domain behavioral Verilog-A only. Do not use user `task`/`endtask`, Verilog-AMS digital kernels, branch current contributions, transistor devices, `ddt()`, or `idt()`. Do not hard-code visible or hidden stimulus times.

## Output Contract

Return only `windowed_event_rate_monitor.va` implementing the public module. The file must compile under Spectre-compatible Verilog-A and must not require additional modules, include files beyond standard disciplines, or testbench changes.
