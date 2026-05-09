Create only the DUT Verilog-A model for `resettable_integrator`. Do not generate a testbench.

Required module: `resettable_integrator`. Ports, all `electrical`, exactly as named and ordered: `vin`, `rst`, `vout`.
Behavior: integrate `vin` into a bounded state while `rst` is low; when `rst` is high, clear the state to zero. Use a Spectre-compatible behavioral implementation and voltage-domain `transition(...)` output.
Public evaluation contract: the fixed harness runs `tran tran stop=320n maxstep=500p`; public waveform columns are `vin`, `rst`, and `vout`.

Return exactly one complete Verilog-A code block for `resettable_integrator.va`.
