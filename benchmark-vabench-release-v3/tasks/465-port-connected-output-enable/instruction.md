# Port Connected Output Enable

Implement one Verilog-A source file named `port_connected_output_enable.va`.

## Required Feature

Use $port_connected() to choose behavior based on optional port binding.

## Required Interface

```verilog
module port_connected_output_enable (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

- Initialize `out`, `metric`, and an internal event counter to zero.
- On each rising crossing of `clk` through 0.45 V:
  - If `rst` is above 0.45 V, clear `out`, `metric`, and the event counter.
  - Otherwise use `$port_connected(out)` to decide whether the output port is connected.
  - When `out` is connected, drive `out = V(vin)` and `metric = 1.0`.
  - When `out` is not connected, the internal selected value should be 0.0 and `metric = 0.0`.
- The repository behavior checker certifies the connected-output path with `out` bound in the Spectre testbench.
- Drive `out` and `metric` with `transition(..., 0, 200p, 200p)`.
- Use only voltage-domain contributions; do not use `I(...)`.

Return exactly one source artifact named `port_connected_output_enable.va`.
