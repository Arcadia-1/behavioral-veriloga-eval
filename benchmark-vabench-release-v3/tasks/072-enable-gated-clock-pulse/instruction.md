# Enable Gated Clock Pulse

Implement `enable_gated_clock_pulse.va` in Verilog-A.

## Interface

```verilog
module enable_gated_clock_pulse(clk, en, pulse);
```

Inputs: `clk, en`.
Outputs: `pulse`.

## Required Behavior

Drive `pulse` high exactly when both `clk` and `en` are high, and low otherwise. The output is a gated clock-level pulse used by public smoke testbenches.

Use logic threshold 0.45 V for digital decisions, drive high outputs to 0.9 V and low outputs to 0 V, and use short transition edges so EVAS transient traces are stable away from switching instants.
