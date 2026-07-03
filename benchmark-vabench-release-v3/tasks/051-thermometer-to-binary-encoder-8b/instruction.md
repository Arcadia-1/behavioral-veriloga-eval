# Thermometer To Binary Encoder 8b

Implement one Verilog-A DUT file named `therm_to_bin_8b.va`.

The DUT is a voltage-domain utility module for analog/mixed-signal testbenches.

## Interface

The file must define module `therm_to_bin_8b` with vector electrical ports in this exact order:

```text
th[255:0], b[7:0], valid
```

Use Verilog-A vector ports, for example:

```verilog
module therm_to_bin_8b(
    input electrical [255:0] th,
    output electrical [7:0] b,
    output electrical valid
);
```

Use these public parameters unless you have a compatible reason to add more:

- `vdd = 0.9`
- `vth = 0.45`
- `tr = 20p`

## Required Behavior

Treat all logic inputs as 0/0.9 V logic using the `vth` threshold. The least
significant thermometer bit is `th[0]`; the most significant thermometer bit is
`th[255]`. The least significant binary output bit is `b[0]`; the most
significant binary output bit is `b[7]`.

Encode `th[255:0]` into an 8-bit count and a `valid` flag. A valid
thermometer input is cumulative from `th[0]`: exactly `th[0]` through
`th[count-1]` are high and all higher thermometer inputs are low. For valid
inputs, drive `b[7:0]` to the unsigned count, where `b[7]` is the most
significant bit. Code 0 is valid and means all thermometer inputs are low. Code
255 is valid and means `th[0]` through `th[254]` are high and `th[255]` is low.

For any non-cumulative bubble, gap, isolated high pattern, or all-256-high
pattern, drive `valid` low and drive `b[7:0]` to zero.

Drive high outputs near `vdd` and low outputs near 0 V. Use smooth Verilog-A
voltage contributions such as `transition(...)`. Compact loop-based Verilog-A is
preferred; do not manually expand 256 scalar input ports.

## Public Smoke

The public smoke test checks interface and simulation viability. The behavioral
contract includes boundary thermometer codes and invalid non-cumulative inputs.

## Output

Return exactly one source artifact named `therm_to_bin_8b.va`. Do not generate a Spectre testbench for this task.
