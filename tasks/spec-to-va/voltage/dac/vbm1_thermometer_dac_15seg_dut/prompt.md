# Task: vbm1_thermometer_dac_15seg_dut

Write a pure voltage-domain Verilog-A DUT for a 4-bit-equivalent, 15-segment
unit-element thermometer DAC.

Return exactly one complete Verilog-A file named
`thermometer_dac_15seg.va`.

## Module Contract

Implement this module declaration and port order:

```verilog
module thermometer_dac_15seg(
    seg0, seg1, seg2, seg3, seg4, seg5, seg6, seg7,
    seg8, seg9, seg10, seg11, seg12, seg13, seg14,
    vref, vss, aout
);
```

All ports are `electrical`. `seg0` through `seg14`, `vref`, and `vss` are
inputs; `aout` is the output. Segment pins use 0 V / 0.9 V logic levels with a
threshold parameter near 0.45 V.

## Required Behavior

- Treat every segment pin above threshold as one active unit element.
- Count all fifteen unary segment pins, including `seg14`.
- Drive `aout` from `vss` to `vref` with endpoint scaling:

```text
aout = vss + (vref - vss) * active_segment_count / 15
```

- Smooth the output contribution with `transition`.
- Stay in the pure voltage-domain behavioral subset. Do not use current
  contributions, `ddt`, or `idt`.

## Public Evaluation Observables

The public checker samples `aout` away from input transitions for active segment
counts 0, 1, 2, 7, 14, and 15. It checks monotonicity, endpoint scaling, and
full-scale behavior when all fifteen segments are active.
