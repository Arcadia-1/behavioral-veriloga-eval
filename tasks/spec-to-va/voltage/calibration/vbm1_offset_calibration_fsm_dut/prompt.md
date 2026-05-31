# Task: vbm1_offset_calibration_fsm_dut

Write a pure voltage-domain Verilog-A module for a offset calibration FSM.

The DUT module is `offset_calibration_fsm` with ports `clk, rst, comp, trim`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required behavior:
- Initialize and reset `trim` to 0.45 V on rising `clk` with `rst` high.
- On each rising clock after reset, add 0.08 V when `comp` is high and subtract 0.08 V when `comp` is low.
- Clamp `trim` to 0.05 V to 0.85 V and drive through `transition()`.

Use voltage contributions only. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `offset_calibration_fsm.va`.
