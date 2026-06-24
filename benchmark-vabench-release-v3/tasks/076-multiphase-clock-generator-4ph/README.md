# Multiphase Clock Generator 4ph

Implement `multiphase_clock_generator_4ph.va` in Verilog-A.

## Interface

```verilog
module multiphase_clock_generator_4ph(clk0, clk90, clk180, clk270);
```

Inputs: `none`.
Outputs: `clk0, clk90, clk180, clk270`.

## Required Behavior

Generate four 0.9 V clocks with 20 ns period and 50 percent duty cycle. Rising edges of `clk90`, `clk180`, and `clk270` must lag `clk0` by 5 ns, 10 ns, and 15 ns respectively.

Use logic threshold 0.45 V for digital decisions, drive high outputs to 0.9 V and low outputs to 0 V, and use short transition edges so EVAS transient traces are stable away from switching instants.
