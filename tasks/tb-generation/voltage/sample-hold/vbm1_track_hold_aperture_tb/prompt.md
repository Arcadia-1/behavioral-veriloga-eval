# Task: vbm1_track_hold_aperture_tb

Write a Spectre testbench for a sample-and-hold with aperture delay DUT.

The DUT module is `sample_hold_aperture_ref` with ports `VDD, VSS, clk, vin, vout`. All ports are electrical; digital-control ports use 0/0.9 V logic levels. The candidate DUT file will be available as `sample_hold_aperture_ref.va`; include it with `ahdl_include` and instantiate the DUT using the exact module and port names.

The testbench must exercise:
- On a rising `clk` edge, schedule sampling after a 200 ps aperture delay.
- At the aperture timer event, capture `vin` and hold it on `vout` until the next sample.
- Drive `vout` with smoothed voltage-domain transitions.

Stimulus and observability requirements:
- Drive a changing input around clock edges so aperture-delayed sampling is distinguishable from immediate sampling.
- Save `clk`, `vin`, and `vout`.

Return exactly one Spectre testbench file named `tb_sample_hold_aperture_ref.scs`.
