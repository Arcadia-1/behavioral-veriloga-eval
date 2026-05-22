# Task: vbm1_vco_phase_integrator_e2e

Write both the Verilog-A DUT and Spectre testbench for a timer-driven VCO phase integrator.

The DUT module is `vco_phase_integrator` with ports `vctrl, phase, clk`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required DUT behavior:
- Use a 1 ns timer update and increment phase by `0.03 + 0.09 * V(vctrl)` at each update.
- Wrap phase at 1.0 and toggle `clk` on each wrap.
- Drive both `phase` and `clk` through `transition()`.

Required testbench behavior:
- Drive `vctrl` through low and higher-control intervals so the late clock edge rate is faster than the early edge rate.
- Save `vctrl`, `phase`, and `clk` across a long transient.

Use voltage contributions only in the Verilog-A DUT. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly two files: `vco_phase_integrator.va` and `tb_vco_phase_integrator_ref.scs`.
