# Task: vbm1_cdac_calibration_dut

Write a pure voltage-domain Verilog-A module for a trim-voltage generator.

The DUT module is `cdac_calibration` with ports `clk, rst, err, trim`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required behavior:
- Implement a voltage-domain calibration accumulator that generates a trim voltage, not a capacitor-array CDAC model.
- Initialize `trim` to 0.45 V and reset it to 0.45 V when `rst` is high at a rising `clk` edge.
- When reset is low, add 0.06 V on high `err`, subtract 0.06 V on low `err`, clamp to 0.05 V to 0.85 V, and drive through `transition()`.

Use voltage contributions only. Do not use current contributions, `ddt()`, or `idt()`.

Review caveat: Historical naming can suggest a full capacitor-array CDAC; this public task is only the voltage-domain calibration accumulator that drives `trim`.

Return exactly one complete Verilog-A file named `cdac_calibration.va`.
