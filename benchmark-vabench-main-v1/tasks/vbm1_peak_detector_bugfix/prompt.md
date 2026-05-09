The following implementation is intentionally wrong because it only mirrors its first input. Fix the behavior without changing the public interface.

```verilog-a
`include "constants.vams"
`include "disciplines.vams"
module peak_detector(vin, rst, vout);
    input vin, rst; output vout;
    electrical vin, rst, vout;
    analog begin V(vout) <+ transition(V(vin), 0, 500p, 500p); end
endmodule

```

Required module: `peak_detector`. Ports, all `electrical`, exactly as named and ordered: `vin, rst, vout`.
Behavior: track and hold the maximum input value until reset. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=180n maxstep=500p` and saves waveform columns `vin rst vout`.

Return exactly one complete Verilog-A code block for module `peak_detector`.
