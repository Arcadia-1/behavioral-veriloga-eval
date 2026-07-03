# Trim Ctrl 5bit

Implement a voltage-domain scalar-to-trim-code encoder for a calibration control word.

## Public Interface

Declare module `trim_ctrl_5bit` with positional ports:

```verilog
module trim_ctrl_5bit(ain, dout0, dout1, dout2, dout3, dout4);
```

All ports are scalar `electrical` voltage-domain ports. `ain` is an analog code-level input. `dout0..dout4` are voltage-coded trim-control bits, with `dout0` as the least significant bit.

## Functional Contract

- Convert `V(ain)` to the nearest integer code.
- Clamp the code to the valid 5-bit trim range `0..31`.
- Drive `dout0..dout4` from the clamped binary code, LSB first.
- Drive high bits near 0.9 V and low bits near 0 V.
- Keep the model deterministic and voltage-domain only.

## Output

Return exactly one source artifact named `trim_ctrl_5bit.va`. Do not generate a Spectre testbench.
