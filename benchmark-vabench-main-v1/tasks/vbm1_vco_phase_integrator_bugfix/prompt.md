The following implementation is intentionally wrong because it only mirrors its first input. Fix the behavior without changing the public interface.

```verilog-a
`include "constants.vams"
`include "disciplines.vams"
module vco_phase_integrator(vctrl, phase, clk);
    input vctrl, phase; output clk;
    electrical vctrl, phase, clk;
    analog begin V(clk) <+ transition(V(vctrl), 0, 500p, 500p); end
endmodule

```

Required module: `vco_phase_integrator`. Ports, all `electrical`, exactly as named and ordered: `vctrl, phase, clk`.
Behavior: integrate control voltage into a wrapped oscillator phase. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=180n maxstep=500p` and saves waveform columns `vctrl phase clk`.

Return exactly one complete Verilog-A code block for module `vco_phase_integrator`.
