# Task: vbm1_gain_trim_controller_bugfix

The provided voltage-domain gain-trim controller updates the control
voltage in the wrong direction relative to the measured error. Fix the
controller so it increases gain control when the measured value is below the
target band and decreases gain control when the measured value is above the
target band.

The fixed module must be named `gain_trim_controller` and use electrical ports
`clk`, `rst`, `meas`, `target`, and `gain_ctrl`. Reset should restore the
control voltage to its nominal starting value. Rising clock edges should update
the control state, and the output should reach and hold both the upper and lower valid trim clamps under sustained error windows.

Use voltage contributions and event-driven state updates. Do not use current
contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `dut_fixed.va`.
