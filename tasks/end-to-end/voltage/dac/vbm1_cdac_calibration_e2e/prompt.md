# Task: vbm1_cdac_calibration_e2e

Write both the Verilog-A DUT and Spectre testbench for a trim-voltage generator.

The DUT module is `cdac_calibration` with ports `clk, rst, err, trim`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required DUT behavior:
- Implement a voltage-domain calibration accumulator that generates a trim voltage, not a capacitor-array CDAC model.
- Initialize `trim` to 0.45 V and reset it to 0.45 V when `rst` is high at a rising `clk` edge.
- When reset is low, add 0.06 V on high `err`, subtract 0.06 V on low `err`, clamp to 0.05 V to 0.85 V, and drive through `transition()`.

Required testbench behavior:
- Use a 20 ns period clock, reset release near 16 ns, and an `err` waveform that is high, low, then high.
- Run to 220 ns with 500 ps maxstep and save `clk`, `rst`, `err`, and `trim`.

Use voltage contributions only in the Verilog-A DUT. Do not use current contributions, `ddt()`, or `idt()`.

Review caveat: Historical naming can suggest a full capacitor-array CDAC; this public task is only the voltage-domain calibration accumulator that drives `trim`.

Return exactly two files: `cdac_calibration.va` and `tb_cdac_calibration_ref.scs`.
