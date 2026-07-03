# Trim Ctrl 4bit

Implement a voltage-domain scalar trim-code decoder.

## Public Interface

Return exactly one Verilog-A source file named `trim_ctrl_4bit.va`. Declare
module `trim_ctrl_4bit` with positional ports `ain, dout0, dout1, dout2,
dout3`. All ports are electrical.

`ain` is an analog code-level input. `dout0..dout3` are voltage-coded trim
control rails ordered from least-significant bit to most-significant bit.

## Functional Contract

Round `ain` to the nearest integer code level and emit the low four bits on
`dout0..dout3`. Active output bits should be near `0.9 V`; inactive output bits
should be near `0 V`. Smooth output transitions with `transition(...)`.

## Modeling Constraints

Use voltage contributions only. Keep the implementation deterministic and
voltage-domain only. Do not modify or emit the support testbench, add checker
logic, hard-code private waveform sample points, add simulator-private side
channels, use current contributions, transistor-level devices, `ddt()`, `idt()`,
or AC/noise-analysis behavior.
