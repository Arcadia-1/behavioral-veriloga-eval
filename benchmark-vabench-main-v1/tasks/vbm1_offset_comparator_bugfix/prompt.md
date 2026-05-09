The following clocked voltage comparator has an offset bug: it ignores the public input offset parameter `vos`.
Fix the behavior without changing the public module name or port list.

```verilog-a
`include "constants.vams"
`include "disciplines.vams"

module cmp_offset_ref(VDD, VSS, CLK, VINP, VINN, OUT_P);
    inout VDD, VSS;
    input CLK, VINP, VINN;
    output OUT_P;
    electrical VDD, VSS, CLK, VINP, VINN, OUT_P;
    parameter real vos = 1m;
    parameter real tt = 20p;
    integer q;
    analog begin
        @(initial_step) q = 0;
        @(cross(V(CLK, VSS) - 0.45, +1)) begin
            q = (V(VINP, VSS) > V(VINN, VSS)) ? 1 : 0;
        end
        V(OUT_P, VSS) <+ V(VDD, VSS) * transition(q ? 1.0 : 0.0, 0, tt, tt);
    end
endmodule

```

Required module: `cmp_offset_ref`.
Ports, all `electrical`, exactly as named and ordered:
`VDD`, `VSS`, `CLK`, `VINP`, `VINN`, `OUT_P`.

Behavior:
- On each rising edge of `CLK`, compare `VINP - VINN` against `vos`.
- Drive `OUT_P` high only when `VINP - VINN > vos`; otherwise drive it low.
- Use voltage-domain contributions and `transition(...)`.
- Do not use current contributions, `ddt()`, or `idt()`.

Public evaluation contract:
- The fixed harness runs `tran tran stop=28n maxstep=20p`.
- Public waveform columns are `CLK`, `VINP`, `VINN`, and `OUT_P`.

Return exactly one complete Verilog-A code block for module `cmp_offset_ref`.
