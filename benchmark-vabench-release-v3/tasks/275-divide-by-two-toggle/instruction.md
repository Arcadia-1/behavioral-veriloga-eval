# Source Divide By Two Toggle

Implement `divide_by_two_toggle.va` in Verilog-A.

## Public Interface

Declare module `divide_by_two_toggle(clk, out)` with scalar electrical
voltage-domain ports. `clk` is the input clock and `out` is the divided toggle
output.

## Public Parameter Contract

- `vth`: rising-edge threshold for `clk`, default `0.45`.
- `vdd`: output high level, default `0.9`.
- `tdel`: output transition delay, default `10p`.
- `tr`: output transition rise/fall time, default `10p`.

## Functional Contract

- Initialize `out` low.
- Toggle the internal output state on every rising crossing of `clk`.
- After the first rising edge, drive `out` high; after the second rising edge,
  drive it low; continue alternating on subsequent rising edges.
- Drive `out` between `0 V` and `vdd` with the public transition delay and
  smoothing time.

## Modeling Constraints

Return only `divide_by_two_toggle.va`. Do not emit a Spectre testbench, checker
logic, private test hooks, or simulator-private side channels. Use
voltage-domain, event-driven Verilog-A; do not use transistor-level devices,
current contributions, `ddt()`, or `idt()`.
