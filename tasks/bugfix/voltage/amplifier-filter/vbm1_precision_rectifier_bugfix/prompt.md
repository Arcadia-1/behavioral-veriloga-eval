# Task: vbm1_precision_rectifier_bugfix

The provided voltage-domain precision rectifier has a negative-half-cycle bug:
negative input voltages are converted into positive output instead of being
blocked at zero. Fix the design so positive input voltages pass through and
negative input voltages drive the output near 0 V.

The fixed module must be named `precision_rectifier` and use electrical ports
`vin` and `vout`. Use the parameter `tr` for the output transition time.

Use voltage contributions and smoothed output transitions. Do not use current
contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `dut_fixed.va`.
