# Task: vbm1_cdac_calibration_tb

Write a Spectre testbench for a trim-voltage generator DUT.

The DUT module is `cdac_calibration` with ports `clk, rst, err, trim`. All ports are electrical; digital-control ports use 0/0.9 V logic levels. The candidate DUT file will be available as `cdac_calibration.va`; include it with `ahdl_include` and instantiate the DUT using the exact module and port names.

The testbench must exercise:
- Implement a voltage-domain calibration accumulator that generates a trim voltage, not a capacitor-array CDAC model.
- Initialize `trim` to 0.45 V and reset it to 0.45 V when `rst` is high at a rising `clk` edge.
- When reset is low, add 0.06 V on high `err`, subtract 0.06 V on low `err`, clamp to 0.05 V to 0.85 V, and drive through `transition()`.

Stimulus and observability requirements:
- Use a 20 ns period clock, reset release near 16 ns, and an `err` waveform that is high, low, then high.
- Run to 220 ns with 500 ps maxstep and save `clk`, `rst`, `err`, and `trim`.

Review caveat: Historical naming can suggest a full capacitor-array CDAC; this public task is only the voltage-domain calibration accumulator that drives `trim`.

Return exactly one Spectre testbench file named `tb_cdac_calibration_ref.scs`.
