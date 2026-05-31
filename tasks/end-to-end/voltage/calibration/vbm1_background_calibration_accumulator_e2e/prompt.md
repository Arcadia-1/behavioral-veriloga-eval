# Task: vbm1_background_calibration_accumulator_e2e

Write both the Verilog-A DUT and Spectre testbench for a background calibration accumulator.

The DUT module is `background_calibration_accumulator` with ports `clk, rst, err, accum`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required DUT behavior:
- Initialize `accum` to 0.45 V and reset it to 0.45 V when `rst` is high at a rising `clk` edge.
- When reset is low, add 0.04 V on each rising `clk` edge if `err` is high, otherwise subtract 0.04 V.
- Clamp the accumulator to the inclusive range 0.05 V to 0.85 V and drive `accum` with `transition()`.

Required testbench behavior:
- Use a 0/0.9 V clock with 20 ns period and a reset that releases near 16 ns.
- Drive `err` high, then low, then high again so the checker sees increment, decrement, and recovery windows.
- Run transient analysis to 220 ns with saved `clk`, `rst`, `err`, and `accum`.

Use voltage contributions only in the Verilog-A DUT. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly two files: `background_calibration_accumulator.va` and `tb_background_calibration_accumulator_ref.scs`.
