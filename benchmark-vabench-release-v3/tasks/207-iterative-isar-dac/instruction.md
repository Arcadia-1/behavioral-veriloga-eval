# Iterative ISAR DAC

Implement `iterative_isar_dac.va` as an iterative SAR-style DAC estimate
generator driven by comparator decisions.

## Public Interface

Use this module signature:

```verilog
module iterative_isar_dac(dcmp, rst, clk, vdac);
```

All ports are electrical. `dcmp` is the comparator decision input, `rst` resets
the search state, `clk` advances the estimate, and `vdac` is the analog estimate
output.

## Public Parameter Contract

- `vth`: logic threshold, default `0.5`.
- `range`: initial search step magnitude, default `0.1`.
- `radix`: step reduction factor after each accepted update, default `2`.
- `lsb`: stop threshold for the iterative search, default `10u`.
- `tr`: output transition time, default `100p`.

## Functional Contract

Initialize `vdac` to zero and the current step to `range`. A rising reset edge
restores both values. On each rising `clk` edge, while the current step is above
`lsb`, move the DAC estimate downward when `dcmp` is high and upward when
`dcmp` is low, then divide the step by `radix`. Once the step has reached the
stop threshold, hold the estimate.

## Modeling Constraints

Use pure voltage-domain event-driven Verilog-A. Do not hard-code testbench
edge times, sample indices, or checker-only expected values.
