# DAC4bit Bipolar 252m

## Task Contract

Implement `dac4bit_bipolar_252m.va` as a continuous 4-bit binary voltage DAC with a bipolar 252 mV full-scale reference.

## Public Verilog-A Interface

Use this module signature:

```verilog
module dac4bit_bipolar_252m(d3, d2, d1, d0, vout);
```

All ports are scalar `electrical` nodes. `d3` is the MSB, `d0` is the LSB, and `vout` is the analog DAC output.

## Public Parameter Contract

- `vref`: bipolar reference magnitude, default `252m`.
- `vtrans`: bit decision threshold, default `0.45`.
- `tdel`: output transition delay, default `0`.
- `trise`: output rise time, default `1p`.
- `tfall`: output fall time, default `1p`.

## Required Behavior

- Decode `d3..d0` as an unsigned 4-bit binary code.
- Map code zero to `-vref`.
- Map code fifteen to `+vref`.
- Use the linear bipolar transfer `vref * (2*code/15 - 1)`.
- Update deterministically when any input bit changes.

## Modeling Constraints

Use voltage-domain behavioral Verilog-A only. Do not hard-code visible stimulus timing, testbench sample points, checker logic, or simulator side channels.

## Output Contract

Return exactly one source artifact named `dac4bit_bipolar_252m.va`.
