# Task: vbm1_slew_rate_limiter_bugfix

The provided voltage-domain slew-rate limiter has a one-sided limiting bug: it
limits upward steps but lets downward input steps jump immediately to the target
voltage. Fix the model so both rising and falling output changes are bounded by
the configured per-update step.

The fixed module must be named `slew_rate_limiter` and use electrical ports
`vin` and `vout`. On each periodic update, if `vin` is above the current output
state by more than the configured step, increase the state by one step. If `vin`
is below the current output state by more than the configured step, decrease the
state by one step. Otherwise, snap to `vin`. The output should be driven through
a smoothed voltage contribution.

Use voltage contributions and smoothed output transitions. Do not use current
contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `dut_fixed.va`.
