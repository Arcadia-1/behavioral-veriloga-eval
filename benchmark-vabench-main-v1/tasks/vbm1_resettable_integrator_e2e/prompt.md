Write a pure Verilog-A resettable integrator and a minimal Spectre testbench.

Required module: `resettable_integrator`. Ports, all `electrical`, exactly as named and ordered: `vin`, `rst`, `vout`.
Behavior: integrate `vin` into a bounded state while `rst` is low; when `rst` is high, clear the state to zero. Use a Spectre-compatible behavioral implementation and voltage-domain `transition(...)` output.
Public evaluation contract: the fixed harness runs `tran tran stop=320n maxstep=500p`; public waveform columns are `vin`, `rst`, and `vout`.

Testbench requirements: include `resettable_integrator.va`, drive reset high at startup and later to clear the state, drive `vin` with a small DC value, instantiate `(vin rst vout)`, save `vin rst vout`, and run exactly `tran tran stop=320n maxstep=500p`. Return one `verilog-a` block and one `spectre` block.
