# Task: vbm1_leaky_hold_bugfix

The provided voltage-domain leaky-hold model has a leakage bug: after a sample
event it keeps the held output level instead of applying the intended gradual
decay. Fix the design so it captures a high held value on each sample edge,
decays while reset is low, and clears promptly when reset is high.

The fixed module must be named `leaky_hold` and use electrical ports `sample`,
`rst`, and `vout`. On a rising `sample` threshold crossing, the held value
should be driven near the configured sampled level. A periodic leakage update
should reduce the held value over time while `rst` is low. When `rst` is high,
the held value and output should clear near zero.

Use voltage contributions and smoothed output transitions. Do not use current
contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `dut_fixed.va`.
