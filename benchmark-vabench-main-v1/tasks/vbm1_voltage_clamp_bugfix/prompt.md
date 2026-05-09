The following Verilog-A module named `voltage_clamp` has a behavioral bug: it is an unconstrained follower and does not clamp.
Fix it without changing the public interface.

```verilog-a
`include "constants.vams"
`include "disciplines.vams"

module voltage_clamp(raw_level, vdd, vss, clamped_level);
    input raw_level, vdd, vss;
    output clamped_level;
    electrical raw_level, vdd, vss, clamped_level;
    parameter real vlo = 0.18;
    parameter real vhi = 0.72;
    parameter real tr = 40p;
    analog begin
        V(clamped_level) <+ transition(V(raw_level), 0.0, tr, tr);
    end
endmodule

```

Core function: voltage clamp.
Behavioral intent: model a bounded analog transfer that follows the input in the middle range and clamps outside public lower/upper limits.

Public interface:
- Module name: `voltage_clamp`.
- Inputs: `raw_level`, `vdd`, `vss`.
- Output: `clamped_level`.
- Public real parameters: `vlo=0.18`, `vhi=0.72`, `tr=40p`.

Compatibility requirements:
- Use voltage-domain electrical ports only.
- Be compatible with real Cadence Spectre.
- Declare port direction and electrical discipline separately.
- Drive output targets with `transition(...)`.
- Do not use current contributions, `ddt()`, or `idt()`.

Public evaluation contract:
- The checker reads public waveform columns `raw_level` and `clamped_level`.
- The fixed testbench exercises below-limit, in-range, and above-limit input regions.
- The fixed harness runs exactly `tran tran stop=120n maxstep=500p`.


Return exactly one fixed Verilog-A file named `dut.va`.
