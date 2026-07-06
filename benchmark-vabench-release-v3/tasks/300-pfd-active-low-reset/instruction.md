# PFD Active Low Reset

## Task Contract
Implement `pfd_active_low_reset.va`, a voltage-domain phase-frequency detector DUT with an external active-low reset input.

## Public Verilog-A Interface
Declare module `pfd_active_low_reset(ref, fb, rstb, up, down)` with scalar electrical ports. Inputs `ref` and `fb` are voltage-coded edge inputs. Input `rstb` is an active-low asynchronous reset. Outputs `up` and `down` are active-high rail-coded PFD state outputs.

## Public Parameter Contract
Provide overrideable public parameters:

- `vth = 0.45 V`: threshold for `ref`, `fb`, and `rstb`.
- `vh = 0.9 V`: logic-high output level.
- `reset_delay = 80 ps from [0:inf)`: delay from the moment both detector states are asserted to the mutual reset event.
- `tr = 10 ps from [0:inf)`: output transition smoothing time.

## Required Behavior
When `rstb` is below `vth`, clear both PFD states and hold both outputs low. While `rstb` is high, a rising crossing of `ref` asserts `up`, and a rising crossing of `fb` asserts `down`. Once both states have occurred, schedule a reset after `reset_delay` and clear both states at that timer event. The reset input must also clear a pending one-sided UP or DOWN state even if the opposite edge has not arrived.

## Modeling Constraints
Use voltage contributions and smooth output transitions. Do not emit or modify support testbenches, add checker logic, hard-code testbench waveform sample points, add simulator side channels, use current contributions, transistor-level devices, `ddt()`, or `idt()`.

## Output Contract
Return exactly one source artifact named `pfd_active_low_reset.va`.
