# Differential Buffer

## Task Contract

Implement a unity-gain differential voltage buffer.

- Form: `dut`
- Level: `L1`
- Category: mixed-signal analog support primitive
- Target artifact: `differential_buffer.va`

## Form-Specific Requirements

Return only the DUT source file. Do not generate a simulation harness, validation script, waveform
postprocessor, or companion support module.

## Public Verilog-A Interface

`differential_buffer.va` must declare:

```verilog
module differential_buffer(VINP, VINN, VOUTP, VOUTN);
input VINP, VINN;
output VOUTP, VOUTN;
electrical VINP, VINN, VOUTP, VOUTN;
```

## Public Parameter Contract

This task has no public Verilog-A parameters.

## Required Behavior

Continuously drive `VOUTP` with `V(VINP)` and `VOUTN` with `V(VINN)`. Preserve
the input common-mode and differential voltage exactly.

## Modeling Constraints

Use direct voltage contributions. Do not swap the outputs, add gain, add
offset, add delay, clip the outputs, or hard-code testbench waveform values.

## Output Contract

Return exactly one source artifact named `differential_buffer.va`.
