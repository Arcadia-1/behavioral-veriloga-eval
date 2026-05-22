# Task: vbm1_vco_phase_integrator_tb

Write a Spectre testbench for a timer-driven VCO phase integrator DUT.

The DUT module is `vco_phase_integrator` with ports `vctrl, phase, clk`. All ports are electrical; digital-control ports use 0/0.9 V logic levels. The candidate DUT file will be available as `vco_phase_integrator.va`; include it with `ahdl_include` and instantiate the DUT using the exact module and port names.

The testbench must exercise:
- Use a 1 ns timer update and increment phase by `0.03 + 0.09 * V(vctrl)` at each update.
- Wrap phase at 1.0 and toggle `clk` on each wrap.
- Drive both `phase` and `clk` through `transition()`.

Stimulus and observability requirements:
- Drive `vctrl` through low and higher-control intervals so the late clock edge rate is faster than the early edge rate.
- Save `vctrl`, `phase`, and `clk` across a long transient.

Return exactly one Spectre testbench file named `tb_vco_phase_integrator_ref.scs`.
