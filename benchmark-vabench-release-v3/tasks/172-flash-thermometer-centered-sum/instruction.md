# Centered Flash-Code Summary

Implement an eight-input voltage-coded flash thermometer summarizer.

## Public Interface

Declare module `flash_thermometer_centered_sum` with positional ports `b0,
b1, b2, b3, b4, b5, b6, b7, dout`. All ports are electrical.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vth = 0.45 V`: digital decision threshold for each thermometer input.
- `gain = 0.1125 V/code`: output step per asserted tap away from the center
  point.

## Functional Contract

Treat each input as logic `1` when its voltage is greater than `vth`,
otherwise logic `0`. Count all asserted taps and drive a centered flash-code
summary on `dout`: four asserted taps is the zero-code point, counts below four
produce negative output, and counts above four produce positive output.

The output should respond continuously to input level changes; this is a
combinational voltage-domain summarizer, not a clocked latch.

## Modeling Constraints

Return only `flash_thermometer_centered_sum.va`. Use voltage contributions
only. Do not modify or emit the support testbench, add checker logic, hard-code
private waveform sample points, add simulator-private side channels, use
current contributions, `ddt()`, or `idt()`.
