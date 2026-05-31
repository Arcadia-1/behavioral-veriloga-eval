# Task: vbm1_offset_comparator_e2e

Write both the Verilog-A DUT and Spectre testbench for a clocked comparator with input offset.

The DUT module is `cmp_offset_ref` with ports `VDD, VSS, CLK, VINP, VINN, OUT_P`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required DUT behavior:
- On each rising `CLK` edge, compare `VINP - VINN` against an internal positive offset threshold.
- Drive `OUT_P` to the supply level for a high decision and to `VSS` for a low decision.
- Use smoothed voltage-domain output transitions.

Required testbench behavior:
- Sweep `VINP` around `VINN` while clocking the comparator.
- Save the clock, differential inputs, and output so low/high/low decisions are visible.

Use voltage contributions only in the Verilog-A DUT. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly two files: `cmp_offset_ref.va` and `tb_comparator_offset_ref.scs`.
