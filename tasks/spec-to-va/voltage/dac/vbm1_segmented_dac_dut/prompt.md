# Task: vbm1_segmented_dac_dut

Write a pure voltage-domain Verilog-A module named `segmented_dac`.

The module has electrical inputs `b0`, `b1`, `t0`, `t1`, `t2` and electrical
output `aout`. Treat `b0`/`b1` as binary LSB controls and `t0`/`t1`/`t2` as
thermometer segment controls. With `vref=0.72`, each binary LSB contributes
`vref/12`, and each thermometer segment contributes four LSB steps. Drive
`aout` with a smoothed voltage transition and use voltage contributions only.

Return exactly one complete Verilog-A file named `segmented_dac.va`.
