The following pure voltage-domain PFD has a reset-race bug: when both `UP` and `DN` become high, the implementation does not promptly reset both states.  Fix it without changing the public module name or ports.

```verilog-a
`include "constants.vams"
`include "disciplines.vams"

module pfd_updn(VDD, VSS, REF, DIV, UP, DN);
    inout VDD, VSS;
    input REF, DIV;
    output UP, DN;
    electrical VDD, VSS, REF, DIV, UP, DN;
    parameter real vth = 0.45;
    parameter real tedge = 20p;
    integer up_state, dn_state;
    analog begin
        @(initial_step) begin
            up_state = 0;
            dn_state = 0;
        end
        @(cross(V(REF) - vth, +1)) up_state = 1;
        @(cross(V(DIV) - vth, +1)) dn_state = 1;
        V(UP) <+ transition(up_state ? V(VDD) : V(VSS), 0, tedge, tedge);
        V(DN) <+ transition(dn_state ? V(VDD) : V(VSS), 0, tedge, tedge);
    end
endmodule

```

Required behavior:
- Rising edge of `REF` asserts `UP`.
- Rising edge of `DIV` asserts `DN`.
- If both states become high, reset both outputs promptly to avoid overlap.
- Use `@(cross(...))` and `transition(...)`.
- Do not use current contributions, `ddt()`, or `idt()`.

Public evaluation contract:
- The fixed harness runs `tran tran stop=300n maxstep=10p errpreset=conservative`.
- Public waveform columns are `ref`, `div`, `up`, and `dn`.

Return exactly one complete Verilog-A code block for module `pfd_updn`.
