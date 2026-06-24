# Edge Interval TDC 8b

Implement `edge_interval_tdc_8b.va` in Verilog-A.

## Interface

```verilog
module edge_interval_tdc_8b(start, stop, valid, code0, code1, code2, code3, code4, code5, code6, code7);
```

Inputs: `start, stop`.
Outputs: `valid, code0, code1, code2, code3, code4, code5, code6, code7`.

## Required Behavior

On each rising `start`, arm the measurement. On the next rising `stop`, assert `valid` and output `code[7:0] = round((stop_time - start_time) / 1 ns)`, saturated to 0..255.

Use logic threshold 0.45 V for digital decisions, drive high outputs to 0.9 V and low outputs to 0 V, and use short transition edges so EVAS transient traces are stable away from switching instants.
