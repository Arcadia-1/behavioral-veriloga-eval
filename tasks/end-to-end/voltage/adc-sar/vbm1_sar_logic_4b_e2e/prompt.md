# Task: vbm1_sar_logic_4b_e2e

Write both the Verilog-A DUT and Spectre testbench for a 4-bit SAR logic sequencer.

The DUT module is `sar_logic_4b` with ports `VDD, VSS, CLKS, DCOMP, DP_DAC_3, DP_DAC_2, DP_DAC_1, DP_DAC_0, RDY`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required DUT behavior:
- Implement a 4-bit successive-approximation state machine clocked by rising `CLKS` edges.
- Resolve the current trial bit from `DCOMP`, advance to the next lower bit, and assert `RDY` after bit 0 is resolved.
- Drive DAC decision pins and `RDY` as 0/0.9 V voltage-domain outputs with `transition()`.

Required testbench behavior:
- Clock the SAR through repeated conversion cycles with comparator decisions that produce code 1010 at the checked window.
- Save `CLKS`, `DCOMP`, all DAC decision pins, and `RDY`.

Use voltage contributions only in the Verilog-A DUT. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly two files: `sar_logic_4b.va` and `tb_sar_logic_4b_ref.scs`.
