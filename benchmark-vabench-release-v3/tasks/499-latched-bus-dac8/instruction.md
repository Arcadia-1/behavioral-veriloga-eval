# Latched Bus DAC8

Implement one Verilog-A source file named `latched_bus_dac8.va`.

## Public Interface

```verilog
module latched_bus_dac8(vclk, b7, b6, b5, b4, b3, b2, b1, b0, vout);
```

All ports are electrical. `vclk` is the update clock. `b7` is the MSB, `b0` is
the LSB, and `vout` is the analog DAC output.

## Public Parameter Contract

- `vth = 0.45 V`: threshold for the clock and input bits.
- `vref = 1.0 V`: full-scale endpoint reference.
- `tr = 20p`: output transition smoothing time.

## Required Behavior

On each rising crossing of `vclk` through `vth`, sample the eight input bits and
latch the unsigned binary code. Hold the previously latched code between update
edges even if the input bus changes. Map code zero to 0 V and code 255 to
`vref`, with monotonic binary-weighted steps between those endpoints.

## Modeling Constraints

Use voltage-domain event-driven Verilog-A. Do not make `vout` transparently
follow the input bus between clock edges, hard-code public testbench times,
private sample points, current contributions, `ddt()`, or `idt()`.
