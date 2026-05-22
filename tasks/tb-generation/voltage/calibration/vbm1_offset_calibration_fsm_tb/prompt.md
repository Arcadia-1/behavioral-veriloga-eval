# Task: vbm1_offset_calibration_fsm_tb

Write a Spectre testbench for a offset calibration FSM DUT.

The DUT module is `offset_calibration_fsm` with ports `clk, rst, comp, trim`. All ports are electrical; digital-control ports use 0/0.9 V logic levels. The candidate DUT file will be available as `offset_calibration_fsm.va`; include it with `ahdl_include` and instantiate the DUT using the exact module and port names.

The testbench must exercise:
- Initialize and reset `trim` to 0.45 V on rising `clk` with `rst` high.
- On each rising clock after reset, add 0.08 V when `comp` is high and subtract 0.08 V when `comp` is low.
- Clamp `trim` to 0.05 V to 0.85 V and drive through `transition()`.

Stimulus and observability requirements:
- Drive comparator decisions high, then low, then high so the trim increases, decreases, and recovers.
- Save `clk`, `rst`, `comp`, and `trim`.

Return exactly one Spectre testbench file named `tb_offset_calibration_fsm_ref.scs`.
