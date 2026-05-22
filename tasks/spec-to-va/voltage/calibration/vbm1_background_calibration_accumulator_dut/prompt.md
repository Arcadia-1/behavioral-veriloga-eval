# Task: vbm1_background_calibration_accumulator_dut

Write a pure voltage-domain Verilog-A module for a background calibration accumulator.

The DUT module is `background_calibration_accumulator` with ports `clk, rst, err, accum`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required behavior:
- Initialize `accum` to 0.45 V and reset it to 0.45 V when `rst` is high at a rising `clk` edge.
- When reset is low, add 0.04 V on each rising `clk` edge if `err` is high, otherwise subtract 0.04 V.
- Clamp the accumulator to the inclusive range 0.05 V to 0.85 V and drive `accum` with `transition()`.

Use voltage contributions only. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `background_calibration_accumulator.va`.
