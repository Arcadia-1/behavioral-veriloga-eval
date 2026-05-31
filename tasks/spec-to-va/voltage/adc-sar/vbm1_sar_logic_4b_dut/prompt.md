# Task: vbm1_sar_logic_4b_dut

Write a pure voltage-domain Verilog-A module for a 4-bit SAR logic sequencer.

The DUT module is `sar_logic_4b` with ports `VDD, VSS, CLKS, DCOMP, DP_DAC_3, DP_DAC_2, DP_DAC_1, DP_DAC_0, RDY`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required behavior:
- Implement a 4-bit successive-approximation state machine clocked by rising `CLKS` edges.
- Resolve the current trial bit from `DCOMP`, advance to the next lower bit, and assert `RDY` after bit 0 is resolved.
- Drive DAC decision pins and `RDY` as 0/0.9 V voltage-domain outputs with `transition()`.

Use voltage contributions only. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `sar_logic_4b.va`.
