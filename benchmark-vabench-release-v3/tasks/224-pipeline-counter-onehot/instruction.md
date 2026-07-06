# Pipeline Counter One-Hot

## Task Contract

- Form: `dut`.
- Level: `L1`.
- Category: pipeline timing/control support.
- Target artifact: `pipeline_counter_onehot.va`.
- Role: modulo-six counter with one-hot phase outputs.
- Output boundary: implement only the requested public Verilog-A DUT artifact.

## Public Verilog-A Interface

Declare the public module exactly as:

```verilog
module pipeline_counter_onehot(clk, dout0, dout1, dout2, s0, s1, s2, s3, s4, s5);
```

`clk` is the counter clock, `dout0..dout2` expose the binary counter code, and `s0..s5` expose one-hot phase outputs. All ports are electrical.

## Public Parameter Contract

No overrideable public parameters are required. Use a 0.45 V falling-edge threshold and 0/0.9 V output levels with smooth transitions.

## Required Behavior

Initialize the counter to zero. On each falling `clk` crossing, advance the counter modulo six. Drive exactly one of `s0..s5` high according to the current phase and drive `dout0..dout2` with the binary representation of the same counter value.

## Modeling Constraints

Use deterministic voltage-domain Verilog-A with voltage contributions and event-driven state where needed. Do not add checker logic, hard-code testbench-only sample times, add simulator-private side channels, use transistor-level devices, or introduce current-domain behavior.

## Output Contract

Return exactly one complete Verilog-A source file named `pipeline_counter_onehot.va`. Do not generate a testbench, checker, waveform postprocessor, companion support module, or explanatory prose outside the requested source artifact.
