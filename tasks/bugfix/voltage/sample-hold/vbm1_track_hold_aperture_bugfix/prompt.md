# Task: vbm1_track_hold_aperture_bugfix

The provided voltage-domain track/hold model has an aperture bug: it samples
`vin` immediately at the rising `clk` edge instead of waiting for the configured
aperture delay. Fix the model so each rising clock edge arms a delayed sample,
then captures `vin` after `taperture` and holds that value until the next
sample event.

The fixed module must be named `sample_hold_aperture_ref` and use electrical
ports `VDD`, `VSS`, `clk`, `vin`, and `vout`. The output should drive the held
sample value with a smoothed voltage transition. The supply pins are available
for interface compatibility, but this task is still a pure voltage-domain
behavioral model.

Use voltage contributions and smoothed output transitions. Do not use current
contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `dut_fixed.va`.
