# Period Meter 16b

Implement `period_meter_16b.va` in Verilog-A.

## Interface

```verilog
module period_meter_16b(clk_in, valid, period0, period1, period2, period3, period4, period5, period6, period7, period8, period9, period10, period11, period12, period13, period14, period15);
```

Inputs: `clk_in`.
Outputs: `valid, period0, period1, period2, period3, period4, period5, period6, period7, period8, period9, period10, period11, period12, period13, period14, period15`.

## Required Behavior

Measure the interval between consecutive rising edges of `clk_in`. After the second and later rising edges, assert `valid` and output the period in 1 ns LSBs on `period[15:0]`.

Use logic threshold 0.45 V for digital decisions, drive high outputs to 0.9 V and low outputs to 0 V, and use short transition edges so EVAS transient traces are stable away from switching instants.
