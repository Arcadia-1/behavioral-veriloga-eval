# Task: vbm1_resettable_integrator_bugfix

The provided voltage-domain resettable integrator fails to clear its accumulated
state during reset. Fix the model so reset immediately holds the integrated
output near zero and the accumulator restarts from zero when reset is released.

The fixed module must be named `resettable_integrator` and use electrical ports
`vin`, `rst`, and `vout`. While reset is low, the model should periodically add
the scaled input contribution to an internal accumulator. The accumulator should
be clamped to the valid output range and driven through a smoothed voltage
transition.

Use voltage contributions and event-driven state updates. Do not use current
contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `dut_fixed.va`.
