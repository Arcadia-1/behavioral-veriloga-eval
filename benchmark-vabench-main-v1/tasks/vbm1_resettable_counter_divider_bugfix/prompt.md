The following clock divider ignores the public division code and reset behavior.
Fix it without changing the public module name or ports.

```verilog-a
`include "constants.vams"
`include "disciplines.vams"

module clk_divider_ref(clk_in, rst_n, div_code_0, div_code_1, div_code_2, div_code_3, div_code_4, div_code_5, div_code_6, div_code_7, clk_out, lock);
    input clk_in, rst_n, div_code_0, div_code_1, div_code_2, div_code_3, div_code_4, div_code_5, div_code_6, div_code_7;
    output clk_out, lock;
    electrical clk_in, rst_n, div_code_0, div_code_1, div_code_2, div_code_3, div_code_4, div_code_5, div_code_6, div_code_7, clk_out, lock;
    parameter real vdd = 0.9;
    parameter real vth = 0.45;
    parameter real trf = 10p;
    integer out_state;
    analog begin
        @(initial_step) out_state = 0;
        @(cross(V(clk_in) - vth, +1)) out_state = !out_state;
        V(clk_out) <+ transition(out_state ? vdd : 0.0, 0, trf, trf);
        V(lock) <+ transition(vdd, 0, trf, trf);
    end
endmodule

```

Required module: `clk_divider_ref`.
Ports, all `electrical`, exactly as named and ordered:
`clk_in`, `rst_n`, `div_code_0` ... `div_code_7`, `clk_out`, `lock`.

Behavior:
- Interpret the eight `div_code_*` inputs as an unsigned division ratio, clamped to at least 1.
- Synchronous active-low reset clears internal count, output state, and `lock`.
- Generate a divided `clk_out` whose edge intervals match the public ratio.
- Assert `lock` after the first complete output period.
- Use voltage-domain contributions and `transition(...)`.

Public evaluation contract:
- The fixed harness runs `tran tran stop=80n maxstep=50p`.
- Public waveform columns include `clk_in`, `rst_n`, `clk_out`, `lock`, and `div_code_0` through `div_code_7`.

Return exactly one complete Verilog-A code block for module `clk_divider_ref`.
