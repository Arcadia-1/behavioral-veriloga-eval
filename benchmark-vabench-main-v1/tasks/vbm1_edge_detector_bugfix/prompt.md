The following implementation is intentionally wrong because it only mirrors its first input. Fix the behavior without changing the public interface.

```verilog-a
`include "constants.vams"
`include "disciplines.vams"
module edge_detector(sig, rst_n, pulse);
    input sig, rst_n; output pulse;
    electrical sig, rst_n, pulse;
    analog begin V(pulse) <+ transition(V(sig), 0, 500p, 500p); end
endmodule

```

Required module: `edge_detector`. Ports, all `electrical`, exactly as named and ordered: `sig, rst_n, pulse`.
Behavior: emit a short pulse on rising input edges. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=180n maxstep=500p` and saves waveform columns `sig rst_n pulse`.

Return exactly one complete Verilog-A code block for module `edge_detector`.
