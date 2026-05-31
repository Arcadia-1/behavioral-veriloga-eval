# Task: vbm1_lock_detector_tb

Write a Spectre testbench for a reference-feedback lock detector DUT.

The DUT module is `lock_detector` with ports `ref_clk, fb_clk, rst_n, lock`. All ports are electrical; digital-control ports use 0/0.9 V logic levels. The candidate DUT file will be available as `lock_detector.va`; include it with `ahdl_include` and instantiate the DUT using the exact module and port names.

The testbench must exercise:
- Use active-low reset to clear lock state and the consecutive-hit counter.
- Record rising feedback-clock edge times and compare them against rising reference-clock edges.
- Assert `lock` after three consecutive reference events whose feedback edge is within 2 ns.

Stimulus and observability requirements:
- Drive initial mismatched or unsettled clocks followed by aligned reference and feedback clocks.
- Save `ref_clk`, `fb_clk`, `rst_n`, and `lock`.

Return exactly one Spectre testbench file named `tb_lock_detector_ref.scs`.
