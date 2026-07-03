# Mixed Logic Clocked Voltage Sampler

Implement one Verilog-AMS source file named `mixed_logic_clocked_voltage_sampler.vams`.

This is an AMS mixed-signal extension task. It intentionally exercises digital/mixed constructs such as `wreal`, `logic`, `assign`, and/or `always`, while remaining behavioral and avoiding transistor-level devices.

## Required Behavior

Combine logic `always` sampling with an analog voltage output.

The module must have this interface:

```verilog
module mixed_logic_clocked_voltage_sampler(vin, clk, en, sel, a, b, vout);
    input vin, clk, en, sel, a, b;
    output vout;
    electrical vin, vout;
    logic clk, en, sel;
    wreal a, b, level;
    logic sampled;
```

On every positive clock edge, sample `en` into the internal logic state:

```verilog
always @(posedge clk) sampled = en;
```

In the analog block, drive `V(vout)` from `V(vin)` when `sampled` is high and from `0.0` when it is low, using `transition(sampled ? V(vin) : 0.0, 0.0, tr, tr)`.

Use the module and port names from the starter. Do not use current-domain `I(...)` contributions or transistor-level primitives.

## Output

Return exactly one source artifact named `mixed_logic_clocked_voltage_sampler.vams`.
