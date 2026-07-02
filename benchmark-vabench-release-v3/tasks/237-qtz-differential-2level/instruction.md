# Differential Two-Level Quantizer

Implement the Verilog-A module `qtz_differential_2level` in `qtz_differential_2level.va`.

## Public Interface

Use the exact module interface:

```verilog
module qtz_differential_2level(vinp, vinn, vrefp, vrefn, clk, dout);
input vinp, vinn, vrefp, vrefn, clk;
output dout;
electrical vinp, vinn, vrefp, vrefn, clk, dout;
```

Public parameters should include `vth=0.45` for clock-edge detection and a small crossing tolerance such as `ttol=5p`.

## Required Behavior

Model a clocked differential quantizer with two signed output levels. On each rising `clk` transition, compute the input difference `vinp-vinn` and the reference midpoint between `vrefn` and `vrefp`. Drive `dout` to `+0.5` when the sampled input difference is above that midpoint threshold; otherwise drive `dout` to `-0.5`. Hold the previous quantized code between clock edges.

## Modeling Contract

The quantizer output is a signed code voltage, not a rail-to-rail logic output. Keep the model event-driven and voltage-domain; do not use transistor-level devices, current injection, hidden test hooks, or checker-specific side channels.
