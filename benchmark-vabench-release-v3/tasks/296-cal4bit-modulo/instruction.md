# CAL4bit Floor-Clamped Encoder

Implement a voltage-domain scalar-to-4-bit calibration encoder.

## Public Interface

Return exactly one Verilog-A source file named `cal4bit_modulo.va`. Declare
module `cal4bit_modulo` with positional ports `ain, d0, d1, d2, d3`. All ports
are electrical.

`ain` is an analog code-level input. `d0..d3` are voltage-coded output bits
ordered from least-significant bit to most-significant bit.

## Public Parameter Contract

Provide overrideable parameter `vh = 0.9 V` for the output logic-high level.

## Functional Contract

Floor the input voltage to an integer code, clamp the code to the valid 4-bit
range `0..15`, and emit the clamped code on `d0..d3`. Active output bits should
be near `vh`; inactive output bits should be near `0 V`. Despite the historical
module name, the public behavior is floor-then-clamp encoding, not modulo
wrapping.

## Modeling Constraints

Use voltage contributions only. Smooth output transitions with
`transition(...)`. Do not modify or emit the support testbench, add checker
logic, hard-code private waveform sample points, add simulator-private side
channels, use current contributions, transistor-level devices, `ddt()`, `idt()`,
or AC/noise-analysis behavior.
