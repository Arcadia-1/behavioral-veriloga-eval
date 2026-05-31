# Task: vbm1_offset_comparator_bugfix

The provided voltage-domain offset comparator applies the decision polarity
incorrectly around its input offset threshold. Fix the comparator so the output
goes high only when `VINP - VINN` exceeds the positive offset value.

The fixed module must be named `cmp_offset_ref` and use electrical ports `VDD`,
`VSS`, `CLK`, `VINP`, `VINN`, and `OUT_P`. On each rising clock crossing, the
model should latch the comparator decision and drive `OUT_P` between `VSS` and
`VDD` using a smoothed voltage transition.

Use voltage contributions and event-driven state updates. Do not use current
contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `dut_fixed.va`.
