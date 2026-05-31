# Task: vbm1_strongarm_comparator_behavior_bugfix

The following voltage-domain StrongArm-style comparator has a reset-priority
bug: clock edges can update the outputs while `rst` is high. Fix the design so
reset has unconditional priority and forces both outputs low.

The fixed module must be named `strongarm_reset_priority_fixed` and use
electrical ports `vdd`, `vss`, `clk`, `rst`, `inp`, `inn`, `outp`, and `outn`.
When `rst` is high, both outputs must remain low. When reset is released, rising
clock edges should compare `inp` and `inn`: `outp` high / `outn` low for
`inp > inn`, and `outn` high / `outp` low for `inn > inp`.

Use voltage contributions and smoothed output transitions. Do not use current
contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `dut_fixed.va`.
