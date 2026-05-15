# Task: vbm1_strongarm_comparator_behavior_dut

Write a pure voltage-domain Verilog-A module named `cmp_strongarm`.

The module is a clocked StrongArm-style comparator with electrical ports
`CLK`, `VINN`, `VINP`, `DCMPN`, `DCMPP`, `LP`, `LM`, `VSS`, and `VDD`. On each
rising edge of `CLK`, compare `VINP - VINN` after applying the optional
`voffset` parameter. Drive `DCMPP` high and `DCMPN` low when the offset-adjusted
differential input is positive; drive `DCMPN` high and `DCMPP` low when it is
negative. On falling clock edges, reset both comparator outputs low.

Use voltage contributions and smoothed output transitions. Do not use current
contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `cmp_strongarm.va`.
