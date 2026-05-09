The following implementation is intentionally wrong because it only mirrors its first input. Fix the behavior without changing the public interface.

```verilog-a
`include "constants.vams"
`include "disciplines.vams"
module debounce_latch(sig, rst_n, out);
    input sig, rst_n; output out;
    electrical sig, rst_n, out;
    analog begin V(out) <+ transition(V(sig), 0, 500p, 500p); end
endmodule

```

Required module: `debounce_latch`. Ports, all `electrical`, exactly as named and ordered: `sig, rst_n, out`.
Behavior: ignore short glitches and assert only after a stable high input. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=140n maxstep=500p` and saves waveform columns `sig rst_n out`.

Return exactly one complete Verilog-A code block for module `debounce_latch`.
