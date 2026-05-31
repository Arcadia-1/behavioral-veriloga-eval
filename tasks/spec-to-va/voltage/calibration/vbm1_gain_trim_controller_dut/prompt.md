# Task: vbm1_gain_trim_controller_dut

Write a pure voltage-domain Verilog-A module for a gain trim controller.

The DUT module is `gain_trim_controller` with ports `clk, rst, meas, target, gain_ctrl`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required behavior:
- Initialize and reset `gain_ctrl` to 0.30 V on rising `clk` while `rst` is high.
- When `meas` is below `target - 0.02`, increase the control by 0.05 V; when above `target + 0.02`, decrease it by 0.05 V.
- Hold inside the deadband, clamp to 0.05 V to 0.85 V, and drive through `transition()`.

Use voltage contributions only. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `gain_trim_controller.va`.
