# DAC7 Code Generator

## Task Contract

- Form: `dut`.
- Level: `L1`.
- Category: data-converter stimulus/control support.
- Target artifact: `dac7_code_generator.va`.
- Role: clocked inverted high-bit DAC stimulus generator.
- Output boundary: implement only the requested public Verilog-A DUT artifact.

## Public Verilog-A Interface

Declare the public module exactly as:

```verilog
module dac7_code_generator(clks, din0, din1, din2, din3, din4, din5, din6);
```

`clks` is the code-update clock and `din0..din6` are voltage-coded code outputs. All ports are electrical.

## Public Parameter Contract

Provide overrideable parameters `vlo = 0`, `vhi = 0.9`, `vth = 0.45`, and `tt = 20p`.

## Required Behavior

Initialize the internal counter to zero and initialize all seven outputs low. On each rising `clks` crossing, first increment an 8-bit counter modulo 256, then publish the inverted high-bit slice using `vlo`/`vhi`:

- `din0 = inverse(counter[7])`
- `din1 = inverse(counter[6])`
- `din2 = inverse(counter[5])`
- `din3 = inverse(counter[4])`
- `din4 = inverse(counter[3])`
- `din5 = inverse(counter[2])`
- `din6 = inverse(counter[1])`

Here `inverse(0)` drives `vhi` and `inverse(1)` drives `vlo`. Hold outputs between clock events.

## Modeling Constraints

Use deterministic voltage-domain Verilog-A with voltage contributions and event-driven state where needed. Do not add checker logic, hard-code testbench-only sample times, add simulator-private side channels, use transistor-level devices, or introduce current-domain behavior.

## Output Contract

Return exactly one complete Verilog-A source file named `dac7_code_generator.va`. Do not generate a testbench, checker, waveform postprocessor, companion support module, or explanatory prose outside the requested source artifact.
