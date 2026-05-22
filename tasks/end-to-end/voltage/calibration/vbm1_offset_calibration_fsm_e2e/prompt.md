# Task: vbm1_offset_calibration_fsm_e2e

Write both the Verilog-A DUT and Spectre testbench for a offset calibration FSM.

The DUT module is `offset_calibration_fsm` with ports `clk, rst, comp, trim`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required DUT behavior:
- Initialize and reset `trim` to 0.45 V on rising `clk` with `rst` high.
- On each rising clock after reset, add 0.08 V when `comp` is high and subtract 0.08 V when `comp` is low.
- Clamp `trim` to 0.05 V to 0.85 V and drive through `transition()`.

Required testbench behavior:
- Drive comparator decisions high, then low, then high so the trim increases, decreases, and recovers.
- Save `clk`, `rst`, `comp`, and `trim`.

Use voltage contributions only in the Verilog-A DUT. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly two files: `offset_calibration_fsm.va` and `tb_offset_calibration_fsm_ref.scs`.
