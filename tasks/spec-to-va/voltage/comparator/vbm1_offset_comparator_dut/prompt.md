# Task: vbm1_offset_comparator_dut

Write a pure voltage-domain Verilog-A module for a clocked comparator with input offset.

The DUT module is `cmp_offset_ref` with ports `VDD, VSS, CLK, VINP, VINN, OUT_P`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required behavior:
- On each rising `CLK` edge, compare `VINP - VINN` against an internal positive offset threshold.
- Drive `OUT_P` to the supply level for a high decision and to `VSS` for a low decision.
- Use smoothed voltage-domain output transitions.

Use voltage contributions only. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `cmp_offset_ref.va`.
