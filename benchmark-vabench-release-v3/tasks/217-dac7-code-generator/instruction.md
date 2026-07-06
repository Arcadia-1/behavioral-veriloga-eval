# DAC7 Code Generator

## Task Contract

- Form: `dut`.
- Level: `L1`.
- Category: data-converter stimulus/control support.
- Target artifact: `dac7_code_generator.va`.
- Role: clocked 7-bit binary code generator.
- Output boundary: implement only the requested public Verilog-A DUT artifact.

## Public Verilog-A Interface

Declare the public module exactly as:

```verilog
module dac7_code_generator(clks, din0, din1, din2, din3, din4, din5, din6);
```

`clks` is the code-update clock and `din0..din6` are voltage-coded code outputs ordered from LSB to MSB. All ports are electrical.

## Public Parameter Contract

Provide overrideable parameters `vlo = 0`, `vhi = 0.9`, `vth = 0.45`, and `tt = 20p`.

## Required Behavior

Initialize the code to zero. On each rising `clks` crossing, increment the 7-bit binary code modulo its range and publish the bits on `din0..din6` using `vlo`/`vhi`. Hold outputs between clock events.

## Modeling Constraints

Use deterministic voltage-domain Verilog-A with voltage contributions and event-driven state where needed. Do not add checker logic, hard-code testbench-only sample times, add simulator-private side channels, use transistor-level devices, or introduce current-domain behavior.

## Output Contract

Return exactly one complete Verilog-A source file named `dac7_code_generator.va`. Do not generate a testbench, checker, waveform postprocessor, companion support module, or explanatory prose outside the requested source artifact.
