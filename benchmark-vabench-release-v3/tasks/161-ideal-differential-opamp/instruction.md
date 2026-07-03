# Ideal Differential Opamp

## Task Contract

Implement an ideal differential-output voltage amplifier centered around a
fixed common-mode.

- Form: `dut`
- Level: `L1`
- Category: mixed-signal analog amplifier primitive
- Target artifact: `ideal_differential_opamp.va`

## Form-Specific Requirements

Return only the DUT source file. Do not generate a simulation harness, validation script, waveform
postprocessor, or companion support module.

## Public Verilog-A Interface

`ideal_differential_opamp.va` must declare:

```verilog
module ideal_differential_opamp(vinp, vinn, voutp, voutn);
input vinp, vinn;
output voutp, voutn;
electrical vinp, vinn, voutp, voutn;
```

## Public Parameter Contract

This task has no public Verilog-A parameters. The common-mode is fixed at
`0.5 V`, and the differential output gain is fixed at `4.0`.

## Required Behavior

Let `vid = V(vinp) - V(vinn)`. Drive the differential outputs symmetrically
around `0.5 V` so that:

- `V(voutp) = 0.5 + 2.0 * vid`
- `V(voutn) = 0.5 - 2.0 * vid`

Equivalently, `V(voutp) - V(voutn) = 4.0 * vid`.

## Modeling Constraints

Use direct voltage contributions. Do not add rail clipping, offset, dynamic
state, bandwidth limits, current contributions, or testbench-specific constants.

## Output Contract

Return exactly one source artifact named `ideal_differential_opamp.va`.
