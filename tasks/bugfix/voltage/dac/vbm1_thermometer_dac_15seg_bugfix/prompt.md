# Task: vbm1_thermometer_dac_15seg_bugfix

Repair the provided pure voltage-domain Verilog-A 4-bit thermometer DAC.

The DUT has fifteen unary segment inputs, `seg0` through `seg14`, plus `vref`,
`vss`, and `aout`. Interpret the segment pins as a 15-segment thermometer code:
each segment above `vth` contributes exactly one unit. Drive `aout` linearly from
`vss` to `vref` using endpoint scaling:

`aout = vss + (vref - vss) * active_segment_count / 15`

The fixed model must count all fifteen unit segments. It must remain purely
voltage-domain, drive `aout` with `transition`, and must not use current
contributions or analog state operators.

