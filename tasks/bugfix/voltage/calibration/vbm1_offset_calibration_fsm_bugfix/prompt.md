# Task: vbm1_offset_calibration_fsm_bugfix

The provided voltage-domain offset calibration FSM has a trim-direction bug.
When reset is asserted, the trim accumulator should return to its nominal
mid-scale value. While reset is released, rising `clk` crossings should update
the trim according to the comparator result: a high `comp` should increase the
trim, and a low `comp` should decrease it. The trim must remain clamped to the
valid output range.

Fix the design so it implements the correct update direction and clamp behavior.
The fixed module must be named `offset_calibration_fsm` and use electrical ports
`clk`, `rst`, `comp`, and `trim`.

Use voltage contributions and smoothed output transitions. Do not use current
contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `dut_fixed.va`.
