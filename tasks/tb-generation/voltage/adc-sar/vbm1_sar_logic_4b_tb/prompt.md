# Task: vbm1_sar_logic_4b_tb

Write a Spectre testbench for a 4-bit SAR logic sequencer DUT.

The DUT module is `sar_logic_4b` with ports `VDD, VSS, CLKS, DCOMP, DP_DAC_3, DP_DAC_2, DP_DAC_1, DP_DAC_0, RDY`. All ports are electrical; digital-control ports use 0/0.9 V logic levels. The candidate DUT file will be available as `sar_logic_4b.va`; include it with `ahdl_include` and instantiate the DUT using the exact module and port names.

The testbench must exercise:
- Implement a 4-bit successive-approximation state machine clocked by rising `CLKS` edges.
- Resolve the current trial bit from `DCOMP`, advance to the next lower bit, and assert `RDY` after bit 0 is resolved.
- Drive DAC decision pins and `RDY` as 0/0.9 V voltage-domain outputs with `transition()`.

Stimulus and observability requirements:
- Clock the SAR through repeated conversion cycles with comparator decisions that produce code 1010 at the checked window.
- Save `CLKS`, `DCOMP`, all DAC decision pins, and `RDY`.

Return exactly one Spectre testbench file named `tb_sar_logic_4b_ref.scs`.
