Given a voltage-domain DUT module `resettable_integrator`, generate only a Spectre testbench. Do not generate Verilog-A modules. Include file: `resettable_integrator.va`. Positional port order: `(vin rst vout)`.

Required module: `resettable_integrator`. Ports, all `electrical`, exactly as named and ordered: `vin`, `rst`, `vout`.
Behavior: integrate `vin` into a bounded state while `rst` is low; when `rst` is high, clear the state to zero. Use a Spectre-compatible behavioral implementation and voltage-domain `transition(...)` output.
Public evaluation contract: the fixed harness runs `tran tran stop=320n maxstep=500p`; public waveform columns are `vin`, `rst`, and `vout`.

Return exactly one fenced `spectre` code block.
