# Analog Multiplier

## Task Contract

Implement a two-input analog voltage multiplier with scalar gain.

- Form: `dut`
- Level: `L1`
- Category: mixed-signal analog arithmetic primitive
- Target artifact: `analog_multiplier_gain.va`

## Form-Specific Requirements

Return only the DUT source file. Do not generate a simulation harness, validation script, waveform
postprocessor, or companion support module.

## Public Verilog-A Interface

`analog_multiplier_gain.va` must declare:

```verilog
module analog_multiplier_gain(sigin1, sigin2, sigout);
input sigin1, sigin2;
output sigout;
electrical sigin1, sigin2, sigout;
```

## Public Parameter Contract

- `gain = 1`: scalar multiplier applied to the analog product. Testbenches may
  override it.

## Required Behavior

Continuously drive `sigout` with `gain * V(sigin1) * V(sigin2)`.

## Modeling Constraints

Use direct voltage-domain arithmetic. Preserve input signs. Do not add offsets,
clipping, filtering, state, current contributions, or testbench-specific
constants.

## Output Contract

Return exactly one source artifact named `analog_multiplier_gain.va`.
