# Windowed Event Rate Monitor

Implement one Verilog-A source file named `windowed_event_rate_monitor.va`.

## Task Contract

Build a Spectre-compatible voltage-domain behavioral DUT source for a clocked
measurement helper that reports event rate and observed average over a
qualified window. Implement only the `windowed_event_rate_monitor` module.

## Public Verilog-A Interface

```verilog
module windowed_event_rate_monitor(clk, rst, event_in, gate, rate, average);
```

All ports are electrical. `clk` is the sampling clock, `rst` is an active-high
reset, `event_in` is a voltage-coded event input, `gate` qualifies the
measurement window, and `rate` and `average` are voltage-coded observables.

## Public Parameter Contract

- `parameter real vth = 0.45`.
- `parameter real vhi = 0.9`.
- `parameter integer window_count = 5`.
- `parameter real tr = 60p`.

## Required Behavior

Initialize `event_count`, `sample_count`, `rate`, and `average` to zero. On each
rising clock crossing, clear the measurement window and both observables when
`rst` is high or `gate <= vth`. Otherwise increment `sample_count`, increment
`event_count` when `event_in > vth`, and drive
`rate = vhi * clip01(event_count / window_count)`.

For the same gated sample window, drive
`average = vhi * clip01(event_count / sample_count)`. Hold the last observable
values between rising clock crossings.

## Modeling Constraints

Use voltage-domain behavioral Verilog-A only. Use local analog helper functions
rather than user `task`/`endtask` syntax. Do not use Verilog-AMS digital
kernels, branch current contributions, transistor devices, `ddt()`, or
`idt()`. Do not hard-code testbench stimulus times.

## Output Contract

Return only `windowed_event_rate_monitor.va` implementing the public module. The file must compile under Spectre-compatible Verilog-A and must not require additional modules, include files beyond standard disciplines, or testbench changes.
