# Task: vbm1_offset_comparator_tb

Write a Spectre testbench for a clocked comparator with input offset DUT.

The DUT module is `cmp_offset_ref` with ports `VDD, VSS, CLK, VINP, VINN, OUT_P`. All ports are electrical; digital-control ports use 0/0.9 V logic levels. The candidate DUT file will be available as `cmp_offset_ref.va`; include it with `ahdl_include` and instantiate the DUT using the exact module and port names.

The testbench must exercise:
- On each rising `CLK` edge, compare `VINP - VINN` against an internal positive offset threshold.
- Drive `OUT_P` to the supply level for a high decision and to `VSS` for a low decision.
- Use smoothed voltage-domain output transitions.

Stimulus and observability requirements:
- Sweep `VINP` around `VINN` while clocking the comparator.
- Save the clock, differential inputs, and output so low/high/low decisions are visible.

Return exactly one Spectre testbench file named `tb_comparator_offset_ref.scs`.
