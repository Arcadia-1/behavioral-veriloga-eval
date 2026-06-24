# Duty Cycle Meter 8b

Implement `duty_cycle_meter_8b.va` in Verilog-A.

## Interface

```verilog
module duty_cycle_meter_8b(clk_in, valid, duty0, duty1, duty2, duty3, duty4, duty5, duty6, duty7);
```

Inputs: `clk_in`.
Outputs: `valid, duty0, duty1, duty2, duty3, duty4, duty5, duty6, duty7`.

## Required Behavior

Measure high time divided by period for each complete cycle of `clk_in`. On the next rising edge, assert `valid` and output `round(255 * high_time / period)` on `duty[7:0]`.

Use logic threshold 0.45 V for digital decisions, drive high outputs to 0.9 V and low outputs to 0 V, and use short transition edges so EVAS transient traces are stable away from switching instants.
