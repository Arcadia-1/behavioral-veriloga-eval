# Task: vbm1_lock_detector_e2e

Write both the Verilog-A DUT and Spectre testbench for a reference-feedback lock detector.

The DUT module is `lock_detector` with ports `ref_clk, fb_clk, rst_n, lock`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required DUT behavior:
- Use active-low reset to clear lock state and the consecutive-hit counter.
- Record rising feedback-clock edge times and compare them against rising reference-clock edges.
- Assert `lock` after three consecutive reference events whose feedback edge is within 2 ns.

Required testbench behavior:
- Drive initial mismatched or unsettled clocks followed by aligned reference and feedback clocks.
- Save `ref_clk`, `fb_clk`, `rst_n`, and `lock`.

Use voltage contributions only in the Verilog-A DUT. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly two files: `lock_detector.va` and `tb_lock_detector_ref.scs`.
