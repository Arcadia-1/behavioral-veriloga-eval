# Configurable Pulse Train Generator

Implement `configurable_pulse_train.va` in Verilog-A.

## Interface

```verilog
module configurable_pulse_train(clk, start, period0, period1, period2, period3, width0, width1, width2, width3, count0, count1, count2, count3, pulse, done);
```

Inputs: `clk, start, period0, period1, period2, period3, width0, width1, width2, width3, count0, count1, count2, count3`.
Outputs: `pulse, done`.

## Required Behavior

On a rising `clk` while idle and `start` is high, capture `period[3:0]`, `width[3:0]`, and `count[3:0]`. Emit exactly `count` pulses, each `width` clock samples wide, with starts separated by `period` clock samples; then assert `done`.

Use logic threshold 0.45 V for digital decisions, drive high outputs to 0.9 V and low outputs to 0 V, and use short transition edges so EVAS transient traces are stable away from switching instants.
