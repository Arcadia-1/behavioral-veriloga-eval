# Clocked DAC Restore 7b

## Task Contract

Implement the single-DUT Verilog-A artifact `clocked_dac_restore_7b.va` for a
clocked seven-bit DAC restoration primitive. The model should sample
voltage-coded input bits on clock events and reconstruct a held bipolar analog
output level.

## Public Verilog-A Interface

The file `clocked_dac_restore_7b.va` must define this positional port order:

```verilog
module clocked_dac_restore_7b(D1, D2, D3, D4, D5, D6, D0, CLK, VOUT);
```

All ports are electrical. `D6` through `D0` are voltage-coded input bits, `CLK`
is the update clock, and `VOUT` is the restored analog output. Preserve the
positional interface above while interpreting `D6` as the MSB and `D0` as the
LSB.

## Public Parameter Contract

- `vth = 0.45 V`: threshold for input bits and rising-clock detection.
- `lsb = 1.8 / 128.0 V`: midrise DAC step size.
- `tr = 20p`: transition smoothing time for `VOUT`.

These parameters may be overridden by the validation harness.

## Required Behavior

On each rising crossing of `CLK` through `vth`, decode the voltage-coded input
word as a seven-bit unsigned code with weights `D6..D0 = 64, 32, 16, 8, 4, 2,
1`. Hold the decoded code between clock edges.

Drive `VOUT` as a bipolar midrise restored level:

```text
VOUT = (code + 0.5) * lsb - 0.9
```

The output should remain stable between updates and use smoothed transitions.

## Modeling Constraints

Use voltage-domain event-driven Verilog-A with voltage contributions only. Do
not use current contributions, transistor-level devices, `ddt()`, `idt()`,
validation logic, auxiliary test hooks, or testbench-specific sample windows
inside the DUT.

## Output Contract

Return exactly one complete Verilog-A source artifact named
`clocked_dac_restore_7b.va`. Do not include explanatory prose outside the source
artifact contents.
