# Task: vbm1_edge_detector_e2e

Write both the Verilog-A DUT and Spectre testbench for a voltage-domain rising
edge detector.

The DUT module must be named `edge_detector` and use electrical ports `sig`,
`rst_n`, and `pulse`. `rst_n` is active low. After reset is released, each
rising crossing of `sig` should generate a short high pulse on `pulse`; falling
crossings must not generate a pulse.

The testbench must stimulate reset and multiple input transitions, save all
public observables, and run a transient analysis suitable for fixed-time pulse
checks.

Return exactly two files: `edge_detector.va` and `tb_edge_detector_ref.scs`.
