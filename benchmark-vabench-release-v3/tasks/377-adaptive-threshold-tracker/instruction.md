# Adaptive Threshold Tracker

Implement one Verilog-A source file named `adaptive_threshold_tracker.va`.

## Task Contract

Build a Spectre-compatible voltage-domain behavioral DUT source for a
comparator-support helper that adapts an observable decision threshold from
sampled input behavior. Implement only the `adaptive_threshold_tracker` module.

## Public Verilog-A Interface

```verilog
module adaptive_threshold_tracker(clk, rst, vin, adapt, trip, threshold_mon, margin_metric);
```

All ports are electrical. `clk` is the sampling clock, `rst` is active-high
reset, `vin` is the sampled analog input, `adapt` is a voltage-coded adaptation
enable, and `trip`, `threshold_mon`, and `margin_metric` are voltage-coded
observables.

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

Initialize the stored threshold to `threshold_init`, `threshold_mon` to
`threshold_init`, and the other observables to zero. On each rising clock
crossing, reset the stored threshold and outputs to those initial values while
`rst` is high. Otherwise compare `vin` against the previously stored threshold:
drive `trip = vhi` when `V(vin) > old_threshold`, otherwise drive `trip = 0 V`.
Drive
`margin_metric = vhi * clip01(abs(V(vin) - old_threshold) / margin_fullscale)`.

When `adapt > vth`, update the stored threshold after the comparison using
`threshold = clamp(adapt_alpha * old_threshold + (1.0 - adapt_alpha) * V(vin),
threshold_min, threshold_max)`. Drive `threshold_mon` with the resulting
next-sample threshold. Hold the last observable values between rising clock
crossings.

## Modeling Constraints

Use voltage-domain behavioral Verilog-A only. Use local analog helper functions
rather than user `task`/`endtask` syntax. Do not use Verilog-AMS digital
kernels, branch current contributions, transistor devices, `ddt()`, or
`idt()`. Do not hard-code testbench stimulus times.

## Output Contract

Return only `adaptive_threshold_tracker.va` implementing the public module. The file must compile under Spectre-compatible Verilog-A and must not require additional modules, include files beyond standard disciplines, or testbench changes.
