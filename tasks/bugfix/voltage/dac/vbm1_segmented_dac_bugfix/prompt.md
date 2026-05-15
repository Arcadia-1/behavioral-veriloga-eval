# Task: vbm1_segmented_dac_bugfix

The provided voltage-domain segmented DAC has a segment-weighting bug: the
thermometer-coded segment bits contribute half of their intended weight. Fix the
DAC so the binary LSBs and thermometer segment bits produce a monotonic output
with the correct 15-step full-scale normalization.

The fixed module must be named `segmented_dac` and use electrical ports `b0`,
`b1`, `t0`, `t1`, `t2`, `vref`, `vss`, and `aout`. The binary bits should
contribute weights 1 and 2, and each thermometer segment bit should contribute
weight 4. The analog output should be referenced to `vss`.

Use voltage contributions and smoothed output transitions. Do not use current
contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `dut_fixed.va`.
