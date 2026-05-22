# Task: vbm1_peak_detector_dut

Write a pure voltage-domain Verilog-A module for a resettable peak detector.

The DUT module is `peak_detector` with ports `vin, rst, vout`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required behavior:
- Track the maximum observed `vin` value using a timer-sampled internal peak.
- High `rst` clears the peak to 0 V.
- Drive `vout` from the peak value through `transition()`.

Use voltage contributions only. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `peak_detector.va`.
