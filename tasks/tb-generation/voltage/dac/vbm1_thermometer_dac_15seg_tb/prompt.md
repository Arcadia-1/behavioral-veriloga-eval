# Task: vbm1_thermometer_dac_15seg_tb

Write a Spectre testbench for a pure voltage-domain Verilog-A DUT named
`thermometer_dac_15seg.va`.

Return exactly one complete Spectre netlist named
`tb_thermometer_dac_15seg_ref.scs`.

## DUT Contract

The candidate DUT is:

```verilog
module thermometer_dac_15seg(
    seg0, seg1, seg2, seg3, seg4, seg5, seg6, seg7,
    seg8, seg9, seg10, seg11, seg12, seg13, seg14,
    vref, vss, aout
);
```

All ports are electrical. Segment inputs are 0 V / 0.9 V logic signals. `vref`
is 0.9 V, `vss` is 0 V, and `aout` should equal
`vss + (vref - vss) * active_segment_count / 15`.

## Required Testbench Behavior

- Include the DUT file with `ahdl_include "thermometer_dac_15seg.va"`.
- Instantiate the DUT with the exact port order above.
- Drive programmed active segment counts 0, 1, 2, 7, 14, and 15.
- Keep samples away from segment transitions so the checker can inspect settled
  values.
- Save `seg0` through `seg14` and `aout`.
- Use a transient stop time of at least 180 ns and a `maxstep` no larger than
  500 ps.

The public checker compares the saved waveform to the expected 15-segment
endpoint-scaled DAC levels and verifies full-scale behavior.
