# Task: vbm1_peak_detector_tb

Write a Spectre testbench for a resettable peak detector DUT.

The DUT module is `peak_detector` with ports `vin, rst, vout`. All ports are electrical; digital-control ports use 0/0.9 V logic levels. The candidate DUT file will be available as `peak_detector.va`; include it with `ahdl_include` and instantiate the DUT using the exact module and port names.

The testbench must exercise:
- Track the maximum observed `vin` value using a timer-sampled internal peak.
- High `rst` clears the peak to 0 V.
- Drive `vout` from the peak value through `transition()`.

Stimulus and observability requirements:
- Apply a first input peak, reset clear, and a second larger peak.
- Save `vin`, `rst`, and `vout`.

Return exactly one Spectre testbench file named `tb_peak_detector_ref.scs`.
