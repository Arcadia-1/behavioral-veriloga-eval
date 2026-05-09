The following module mirrors `trig` instead of generating a fixed-width one-shot pulse. Fix it without changing the public interface.

```verilog-a
`include "constants.vams"
`include "disciplines.vams"
module one_shot_timer(trig, rst_n, pulse);
    input trig, rst_n; output pulse; electrical trig, rst_n, pulse;
    analog begin V(pulse) <+ transition(V(trig), 0, 200p, 200p); end
endmodule

```

Required module: `one_shot_timer`. Ports, all `electrical`, exactly as named and ordered: `trig`, `rst_n`, `pulse`.
Behavior: on each rising edge of `trig`, when `rst_n` is high, emit a fixed-width pulse of duration `tpw`; active-low reset clears the pulse. Use `@(cross(...))`, `timer(...)`, voltage-domain contributions, and `transition(...)`.
Public evaluation contract: the fixed harness runs `tran tran stop=260n maxstep=500p`; public waveform columns are `trig`, `rst_n`, and `pulse`.

Return exactly one complete Verilog-A code block for module `one_shot_timer`.
