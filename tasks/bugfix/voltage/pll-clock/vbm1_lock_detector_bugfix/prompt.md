# Task: vbm1_lock_detector_bugfix

The provided voltage-domain PLL lock detector has a lock assertion off-by-one
bug. It should assert `lock` after the configured number of consecutive
reference-clock edges each observe a recent feedback-clock edge within the
configured time tolerance.

Fix the design so reset clears the internal feedback timestamp, streak counter,
and lock state. While reset is released, every rising `fb_clk` crossing records
the feedback edge time, and every rising `ref_clk` crossing increments the
streak only when the most recent feedback edge is within `tol`. The fixed design
must assert `lock` as soon as the streak reaches `need`.

The fixed module must be named `lock_detector` and use electrical ports
`ref_clk`, `fb_clk`, `rst_n`, and `lock`. Use voltage contributions and smoothed
output transitions. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `dut_fixed.va`.
