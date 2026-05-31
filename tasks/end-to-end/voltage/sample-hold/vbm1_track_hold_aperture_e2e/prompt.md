# Task: vbm1_track_hold_aperture_e2e

Write both the Verilog-A DUT and Spectre testbench for a sample-and-hold with aperture delay.

The DUT module is `sample_hold_aperture_ref` with ports `VDD, VSS, clk, vin, vout`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required DUT behavior:
- On a rising `clk` edge, schedule sampling after a 200 ps aperture delay.
- At the aperture timer event, capture `vin` and hold it on `vout` until the next sample.
- Drive `vout` with smoothed voltage-domain transitions.

Required testbench behavior:
- Drive a changing input around clock edges so aperture-delayed sampling is distinguishable from immediate sampling.
- Save `clk`, `vin`, and `vout`.

Use voltage contributions only in the Verilog-A DUT. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly two files: `sample_hold_aperture_ref.va` and `tb_sample_hold_aperture_ref.scs`.
