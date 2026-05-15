# Task: vbm1_segmented_dac_e2e

Write both the Verilog-A DUT and Spectre testbench for a small voltage-domain
segmented DAC.

The DUT module must be named `segmented_dac` and use electrical ports `b0`,
`b1`, `t0`, `t1`, `t2`, and `aout`. Treat `b0`/`b1` as binary LSB controls and
`t0`/`t1`/`t2` as thermometer segment controls. With `vref=0.72`, each binary
LSB contributes `vref/12`, and each thermometer segment contributes four LSB
steps.

The testbench must apply enough codes to show monotonic levels and save all
public observables.

Return `segmented_dac.va` and `tb_segmented_dac_ref.scs`.
