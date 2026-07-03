# Level Shifter Offset

## Task Contract

Implement a voltage-domain level shifter with an additive offset parameter.

- Form: `dut`
- Level: `L1`
- Category: analog primitive
- Target artifact: `level_shifter_offset.va`

## Form-Specific Requirements

Return only the DUT source file. Do not generate a simulation harness, validation script, waveform
postprocessor, or companion support module.

## Public Verilog-A Interface

`level_shifter_offset.va` must declare:

```verilog
module level_shifter_offset(sigin, sigout);
input sigin;
output sigout;
electrical sigin, sigout;
```

## Public Parameter Contract

- `sigshift = 0.35`: additive output offset in volts. Testbenches may override
  it.

## Required Behavior

Continuously drive `sigout` with `V(sigin) + sigshift`.

## Modeling Constraints

Use direct voltage-domain arithmetic. Do not add gain, clipping, filtering,
state, current contributions, or testbench-specific waveform values.

## Output Contract

Return exactly one source artifact named `level_shifter_offset.va`.
