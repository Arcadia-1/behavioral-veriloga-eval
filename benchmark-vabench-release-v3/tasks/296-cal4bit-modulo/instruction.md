# CAL4bit Floor-Clamped Encoder

## Task Contract

- Form: `dut`
- Level: `L1`
- Category: Calibration, Trim, and DEM Control
- Base function: scalar-to-4-bit calibration encoder
- Domain: `voltage`
- Target artifact(s): `cal4bit_modulo.va`
- Output boundary: implement only the requested DUT artifact; validation harnesses and simulator-private hooks are external to the requested output.

## Form-Specific Requirements

- Return exactly one Verilog-A source file named `cal4bit_modulo.va`.
- Preserve the public module name, positional port order, electrical disciplines, output bit order, and floor-then-clamp behavior.
- Do not generate or modify a Spectre testbench.

## Public Verilog-A Interface

Declare module `cal4bit_modulo` with positional ports:

```verilog
module cal4bit_modulo(ain, d0, d1, d2, d3);
```

All ports are electrical. `ain` is an analog code-level input. `d0..d3` are
voltage-coded output bits ordered from least-significant bit to
most-significant bit.

## Public Parameter Contract

Provide overrideable parameter `vh = 0.9 V` for the output logic-high level.

## Required Behavior

Floor the input voltage to an integer code, clamp the code to the valid 4-bit
range `0..15`, and emit the clamped code on `d0..d3`. Active output bits should
be near `vh`; inactive output bits should be near `0 V`. Despite the historical
module name, the public behavior is floor-then-clamp encoding, not modulo
wrapping.

## Modeling Constraints

Use voltage contributions only. Smooth output transitions with
`transition(...)`. Do not add checker logic, hard-code private waveform sample
points, add simulator-private side channels, use current contributions,
transistor-level devices, `ddt()`, `idt()`, or AC/noise-analysis behavior.

## Output Contract

Return exactly one complete Verilog-A file named `cal4bit_modulo.va`.
Do not include explanatory prose outside the source artifact contents.
