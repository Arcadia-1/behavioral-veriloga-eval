# Task: vbm1_peak_detector_bugfix

The provided voltage-domain peak detector has a reset bug: reset does not clear
the stored peak value. Fix the model so it tracks the highest input voltage
observed while reset is low, clears promptly when reset is high, and can capture
a new peak after reset is released.

The fixed module must be named `peak_detector` and use electrical ports `vin`,
`rst`, and `vout`. On periodic update events, if `rst` is above the logic
threshold the stored peak and output should clear near zero. Otherwise, the
stored peak should update only when `vin` exceeds the current stored peak. The
output should be driven through a smoothed voltage contribution.

Use voltage contributions and smoothed output transitions. Do not use current
contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `dut_fixed.va`.
