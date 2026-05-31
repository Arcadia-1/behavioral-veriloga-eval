# Task: vbm1_gain_trim_controller_e2e

Write both the Verilog-A DUT and Spectre testbench for a gain trim controller.

The DUT module is `gain_trim_controller` with ports `clk, rst, meas, target, gain_ctrl`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required DUT behavior:
- Initialize and reset `gain_ctrl` to 0.30 V on rising `clk` while `rst` is high.
- When `meas` is below `target - 0.02`, increase the control by 0.05 V; when above `target + 0.02`, decrease it by 0.05 V.
- Hold inside the deadband, clamp to 0.05 V to 0.85 V, and drive through `transition()`.

Required testbench behavior:
- Provide target and measured waveforms that create low-measured and high-measured windows long enough to hit both clamps.
- Run transient analysis with clocked samples through trim increase, upper clamp, trim decrease, and lower clamp phases.

Use voltage contributions only in the Verilog-A DUT. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly two files: `gain_trim_controller.va` and `tb_gain_trim_controller_ref.scs`.
