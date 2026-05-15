# Task: vbm1_cdac_calibration_bugfix

The provided voltage-domain CDAC calibration trim controller updates its trim in
the wrong direction when the error input is asserted. Fix the controller so
rising clock edges increase the trim when `err` is high and decrease it when
`err` is low.

The fixed module must be named `cdac_calibration` and use electrical ports
`clk`, `rst`, `err`, and `trim`. Reset should restore `trim` to the nominal
mid-scale value. The trim output must remain bounded in the valid calibration
range and should be driven as a smoothed voltage.

Use voltage contributions and event-driven state updates. Do not use current
contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `dut_fixed.va`.
