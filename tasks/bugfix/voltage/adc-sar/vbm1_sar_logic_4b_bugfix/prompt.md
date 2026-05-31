# Task: vbm1_sar_logic_4b_bugfix

The provided voltage-domain 4-bit SAR logic has an end-of-conversion timing bug:
it asserts `RDY` one clock before the LSB trial has been decided. Fix the
controller so `RDY` remains low through the MSB, next-bit, and LSB-trial setup
states, then asserts only after all four comparator decisions have been applied.

The fixed module must be named `sar_logic_4b` and use electrical ports `VDD`,
`VSS`, `CLKS`, `DCOMP`, `DP_DAC_3`, `DP_DAC_2`, `DP_DAC_1`, `DP_DAC_0`, and
`RDY`. It should start each conversion by trying the MSB, step through bits
3-to-0 on rising `CLKS` crossings, drive DAC decision outputs with voltage
contributions referenced to `VSS`, and clear `RDY` when the next conversion
starts.

Use voltage contributions and smoothed output transitions. Do not use current
contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `dut_fixed.va`.
