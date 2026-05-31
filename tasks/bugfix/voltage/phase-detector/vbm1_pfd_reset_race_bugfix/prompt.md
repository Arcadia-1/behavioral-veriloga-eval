# Task: vbm1_pfd_reset_race_bugfix

The provided voltage-domain phase-frequency detector has a reset-race bug: one
input-edge branch does not clear both UP and DN when the opposite state is
already asserted. Fix the detector so either edge order produces only a short
UP or DN pulse and never leaves both outputs high.

The fixed module must be named `pfd_updn` and use electrical ports `VDD`, `VSS`,
`REF`, `DIV`, `UP`, and `DN`. A rising `REF` edge should set UP; a rising `DIV`
edge should set DN. Whenever both states would be high, both outputs must reset
low in the same event update.

Use voltage contributions and smoothed output transitions. Do not use current
contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `dut_fixed.va`.
