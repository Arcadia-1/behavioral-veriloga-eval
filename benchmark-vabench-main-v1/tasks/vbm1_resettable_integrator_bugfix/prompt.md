The following module is an input follower and does not integrate or reset state. Fix it without changing the public interface.

```verilog-a
`include "constants.vams"
`include "disciplines.vams"
module resettable_integrator(vin, rst, vout);
    input vin, rst; output vout; electrical vin, rst, vout;
    analog begin V(vout) <+ transition(V(vin), 0, 500p, 500p); end
endmodule

```

Required module: `resettable_integrator`. Ports, all `electrical`, exactly as named and ordered: `vin`, `rst`, `vout`.
Behavior: integrate `vin` into a bounded state while `rst` is low; when `rst` is high, clear the state to zero. Use a Spectre-compatible behavioral implementation and voltage-domain `transition(...)` output.
Public evaluation contract: the fixed harness runs `tran tran stop=320n maxstep=500p`; public waveform columns are `vin`, `rst`, and `vout`.

Return exactly one complete Verilog-A code block for module `resettable_integrator`.
