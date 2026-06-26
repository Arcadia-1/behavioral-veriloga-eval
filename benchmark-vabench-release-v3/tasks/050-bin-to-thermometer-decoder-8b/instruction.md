# Bin To Thermometer Decoder 8b

Implement one Verilog-A DUT file named `bin_to_therm_8b.va`.

The DUT is a voltage-domain utility decoder used by analog/mixed-signal testbenches to expand an 8-bit binary code into a 256-line thermometer bus.

## Interface

Define module `bin_to_therm_8b` with vector electrical ports in this exact order:

```verilog
module bin_to_therm_8b(
    input electrical en,
    input electrical [7:0] b,
    output electrical [255:0] th
);
```

Use `vdd=0.9`, `vth=0.45`, and `tr=20p` unless compatible parameters are needed.

## Required Behavior

Treat `en` and `b[7:0]` as 0/0.9 V logic using `vth`. Decode `b[7:0]` as an unsigned integer from 0 to 255, where `b[7]` is the most significant bit.

When `en` is high, drive exactly `code` thermometer outputs high. The high outputs must be cumulative from the low end of the bus: `th[0]` through `th[code-1]` are high, and all higher bits are low. Code 0 drives all thermometer outputs low. Code 255 drives `th[0]` through `th[254]` high and `th[255]` low.

When `en` is low, drive all thermometer outputs low regardless of the binary code.

Drive high outputs near `vdd` and low outputs near 0 V using smooth Verilog-A contributions such as `transition(...)`. Compact loop-based Verilog-A is preferred; do not manually expand 256 scalar output ports.

## Public Smoke

The public smoke test checks interface and simulation viability; hidden tests exercise enable gating and multiple binary codes.

## Output

Return exactly one source artifact named `bin_to_therm_8b.va`. Do not generate a Spectre testbench.
