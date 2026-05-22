# Task: vbm1_gain_trim_controller_tb

Write a Spectre testbench for a gain trim controller DUT.

The DUT module is `gain_trim_controller` with ports `clk, rst, meas, target, gain_ctrl`. All ports are electrical; digital-control ports use 0/0.9 V logic levels. The candidate DUT file will be available as `gain_trim_controller.va`; include it with `ahdl_include` and instantiate the DUT using the exact module and port names.

The testbench must exercise:
- Initialize and reset `gain_ctrl` to 0.30 V on rising `clk` while `rst` is high.
- When `meas` is below `target - 0.02`, increase the control by 0.05 V; when above `target + 0.02`, decrease it by 0.05 V.
- Hold inside the deadband, clamp to 0.05 V to 0.85 V, and drive through `transition()`.

Stimulus and observability requirements:
- Provide target and measured waveforms that create low-measured and high-measured windows long enough to hit both clamps.
- Run transient analysis with clocked samples through trim increase, upper clamp, trim decrease, and lower clamp phases.

Return exactly one Spectre testbench file named `tb_gain_trim_controller_ref.scs`.
