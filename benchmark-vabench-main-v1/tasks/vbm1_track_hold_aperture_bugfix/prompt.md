The following sample-and-hold module ignores the required aperture delay and samples immediately at the clock edge.
Fix it without changing the public module name or ports.

```verilog-a
`include "constants.vams"
`include "disciplines.vams"

module sample_hold_aperture_ref(VDD, VSS, clk, vin, vout);
    inout VDD, VSS;
    input clk, vin;
    output vout;
    electrical VDD, VSS, clk, vin, vout;
    parameter real vth = 0.45;
    parameter real taperture = 200p;
    parameter real tedge = 50p;
    real sampled;
    analog begin
        @(initial_step) sampled = V(vin);
        @(cross(V(clk) - vth, +1)) sampled = V(vin);
        V(vout) <+ transition(sampled, 0.0, tedge, tedge);
    end
endmodule

```

Required module: `sample_hold_aperture_ref`.
Ports, all `electrical`, exactly as named and ordered:
`VDD`, `VSS`, `clk`, `vin`, `vout`.

Behavior:
- On each rising edge of `clk`, arm a sample event at `$abstime + taperture`.
- At that aperture event, capture `vin` and hold it on `vout` until the next capture.
- Use voltage-domain contributions and `transition(...)`.
- Do not use current contributions, `ddt()`, or `idt()`.

Public evaluation contract:
- The fixed harness runs `tran tran stop=140n maxstep=100p`.
- Public waveform columns are `vin`, `clk`, and `vout`.

Return exactly one complete Verilog-A code block for module `sample_hold_aperture_ref`.
