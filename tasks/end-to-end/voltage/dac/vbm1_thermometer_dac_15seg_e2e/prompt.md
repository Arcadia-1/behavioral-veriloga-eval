# Task: vbm1_thermometer_dac_15seg_e2e

Build a complete Verilog-A plus Spectre testbench pair for a pure
voltage-domain 4-bit-equivalent, 15-segment unit-element thermometer DAC.

Return exactly these two files:

- `thermometer_dac_15seg.va`
- `tb_thermometer_dac_15seg_ref.scs`

## DUT Module Contract

Implement this Verilog-A module declaration and port order:

```verilog
module thermometer_dac_15seg(
    seg0, seg1, seg2, seg3, seg4, seg5, seg6, seg7,
    seg8, seg9, seg10, seg11, seg12, seg13, seg14,
    vref, vss, aout
);
```

All ports are `electrical`. `seg0` through `seg14`, `vref`, and `vss` are
inputs; `aout` is the output. Segment pins use 0 V / 0.9 V logic levels.

The DUT must count every active unary segment pin and drive:

```text
aout = vss + (vref - vss) * active_segment_count / 15
```

Use `transition` on the voltage output. Do not use current contributions,
`ddt`, or `idt`.

## Testbench Contract

The Spectre testbench must include `thermometer_dac_15seg.va`, instantiate the
DUT with the exact port order, set `vref=0.9 V` and `vss=0 V`, and program
active segment counts 0, 1, 2, 7, 14, and 15. Save `seg0` through `seg14` and
`aout`.

The public checker samples away from input transitions and verifies the
15-segment endpoint-scaled levels, monotonicity, and the all-segments
full-scale point.
