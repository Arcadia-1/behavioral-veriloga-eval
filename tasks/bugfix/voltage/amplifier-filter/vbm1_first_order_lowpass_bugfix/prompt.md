# Task: vbm1_first_order_lowpass_bugfix

The provided voltage-domain first-order low-pass filter uses the wrong update
coefficient, so its step response settles much more slowly than the intended
time constant. Fix the model so each periodic update moves the output state
toward the input by the configured first-order coefficient.

The fixed module must be named `first_order_lowpass` and use electrical ports
`vin` and `vout`. It should initialize the filter state to zero, update the
state on a periodic timer, and drive `vout` as a smoothed voltage.

Use voltage contributions and event-driven state updates. Do not use current
contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `dut_fixed.va`.
