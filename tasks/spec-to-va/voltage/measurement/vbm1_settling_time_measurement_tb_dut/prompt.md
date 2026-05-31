# Task: vbm1_settling_time_measurement_tb_dut

Write a pure voltage-domain Verilog-A module for a settling response measurement helper.

The DUT module is `settling_time_measurement_tb` with ports `step, vout, done`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required behavior:
- Use a 1 ns timer update with `y += 0.04 * (V(step) - y)` to model a settling response.
- Drive `vout` from `y`; assert `done` only after 120 ns and once `y` is above 0.75 V.
- This is a measurement-helper behavior task, not a true bugfix task.

Use voltage contributions only. Do not use current contributions, `ddt()`, or `idt()`.

Review caveat: This is a normal measurement-helper behavior task. It is not a bugfix task; exact 120 ns boundary semantics belong in conformance.

Return exactly one complete Verilog-A file named `settling_time_measurement_tb.va`.
