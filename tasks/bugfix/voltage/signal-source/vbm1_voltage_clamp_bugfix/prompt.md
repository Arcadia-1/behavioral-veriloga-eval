# Task: vbm1_voltage_clamp_bugfix

The provided voltage-domain clamp model has a lower-bound clamp bug: input
levels below the configured low limit pass through instead of being clipped.
Fix the design so the output follows the raw input only inside the allowed
range, clips low inputs to the low limit, and clips high inputs to the high
limit.

The fixed module must be named `voltage_clamp` and use electrical ports
`raw_level`, `vdd`, `vss`, and `clamped_level`. Use the parameters `vlo`, `vhi`,
and `tr` for the low clamp, high clamp, and output transition time. The expected
default clamp range is 0.18 V to 0.72 V.

Use voltage contributions and smoothed output transitions. Do not use current
contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `dut_fixed.va`.
