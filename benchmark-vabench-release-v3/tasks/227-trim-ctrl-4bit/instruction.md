# Trim Ctrl 4bit

## Task Contract

- Form: `dut`
- Level: `L1`
- Category: Calibration, Trim, and DEM Control
- Base function: scalar trim-code decoder
- Domain: `voltage`
- Target artifact(s): `trim_ctrl_4bit.va`
- Output boundary: implement only the requested DUT artifact; validation harnesses and simulator-private hooks are external to the requested output.

## Form-Specific Requirements

- Return exactly one Verilog-A source file named `trim_ctrl_4bit.va`.
- Preserve the public module name, positional port order, electrical disciplines, and output bit order.
- Do not generate or modify a Spectre testbench.

## Public Verilog-A Interface

Declare module `trim_ctrl_4bit` with positional ports:

```verilog
module trim_ctrl_4bit(ain, dout0, dout1, dout2, dout3);
```

All ports are electrical. `ain` is an analog code-level input. `dout0..dout3`
are voltage-coded trim control rails ordered from least-significant bit to
most-significant bit.

## Public Parameter Contract

No overrideable public parameters are required. Drive active output bits near
0.9 V and inactive output bits near 0 V.

## Required Behavior

Round `ain` to the nearest integer code level and emit the low four bits on
`dout0..dout3`. Smooth output transitions with `transition(...)`.

## Modeling Constraints

Use voltage contributions only. Keep the implementation deterministic and
voltage-domain only. Do not add checker logic, hard-code private waveform
sample points, add simulator-private side channels, use current contributions,
transistor-level devices, `ddt()`, `idt()`, or AC/noise-analysis behavior.

## Output Contract

Return exactly one complete Verilog-A file named `trim_ctrl_4bit.va`.
Do not include explanatory prose outside the source artifact contents.
