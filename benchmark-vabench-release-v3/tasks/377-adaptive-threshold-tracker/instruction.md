# Adaptive Threshold Tracker

Implement one Verilog-A source file named `adaptive_threshold_tracker.va`.

## Task Contract

Build a Spectre-compatible voltage-domain behavioral model for Comparator-support helper that adapts an observable decision threshold from sampled input behavior.

## Form-Specific Requirements

This is a DUT source task. Implement only the `adaptive_threshold_tracker` module; no external testbench, checker logic, transistor devices, or extra helper module is part of the requested artifact.

## Public Verilog-A Interface

```verilog
module adaptive_threshold_tracker(clk, rst, vin, adapt, trip, threshold_mon, margin_metric);
```

## Public Parameter Contract

- `parameter real vth = 0.45`.
- `parameter real vhi = 0.9`.
- `parameter real threshold_init = 0.45`.
- `parameter real threshold_min = 0.25`.
- `parameter real threshold_max = 0.70`.
- `parameter real adapt_alpha = 0.75`.
- `parameter real margin_fullscale = 0.45`.
- `parameter real tr = 60p`.

## Required Behavior

- Compare vin to the previously stored threshold on each rising clock crossing.
- When adapt is high, update the threshold with the public clipped IIR rule after the comparison.
- Report the next-sample threshold on threshold_mon.
- Clear threshold and outputs on reset.
- Use local analog helper functions rather than user task/endtask syntax.

## Modeling Constraints

Use voltage-domain behavioral Verilog-A only. Do not use user `task`/`endtask`, Verilog-AMS digital kernels, branch current contributions, transistor devices, `ddt()`, or `idt()`. Do not hard-code visible or hidden stimulus times.

## Output Contract

Return only `adaptive_threshold_tracker.va` implementing the public module. The file must compile under Spectre-compatible Verilog-A and must not require additional modules, include files beyond standard disciplines, or testbench changes.
