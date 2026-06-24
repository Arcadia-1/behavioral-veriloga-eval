# Ready/Valid Latency Counter 12b

Implement `ready_valid_latency_counter_12b.va` in Verilog-A.

## Interface

```verilog
module ready_valid_latency_counter_12b(clk, valid_i, ready_i, done, lat0, lat1, lat2, lat3, lat4, lat5, lat6, lat7, lat8, lat9, lat10, lat11);
```

Inputs: `clk, valid_i, ready_i`.
Outputs: `done, lat0, lat1, lat2, lat3, lat4, lat5, lat6, lat7, lat8, lat9, lat10, lat11`.

## Required Behavior

On rising `clk`, start counting when `valid_i` is high. Count clock cycles while waiting for `ready_i`; when `ready_i` is sampled high, assert `done` and output the latency count on `lat[11:0]`.

Use logic threshold 0.45 V for digital decisions, drive high outputs to 0.9 V and low outputs to 0 V, and use short transition edges so EVAS transient traces are stable away from switching instants.
