# Phase Detector Chopper

## Task Contract

Implement a chopper-style phase detector primitive that flips RF input polarity
according to the local oscillator sign.

- Form: `dut`
- Level: `L1`
- Category: RF/baseband signal-processing primitive
- Target artifact: `phase_detector_chopper.va`

## Form-Specific Requirements

Return only the DUT source file. Do not generate a simulation harness, validation script, waveform
postprocessor, or companion support module.

## Public Verilog-A Interface

`phase_detector_chopper.va` must declare:

```verilog
module phase_detector_chopper(vlocal_osc, vin_rf, vif);
input vlocal_osc, vin_rf;
output vif;
electrical vlocal_osc, vin_rf, vif;
```

## Public Parameter Contract

- `gain = 1.25`: scalar conversion gain from RF input to IF output.

## Required Behavior

If `V(vlocal_osc)` is strictly positive, drive `vif` with
`gain * V(vin_rf)`. If `V(vlocal_osc)` is zero or negative, drive `vif` with
`-gain * V(vin_rf)`.

## Modeling Constraints

Use direct voltage-domain arithmetic. Do not add filtering, oscillator
generation, phase accumulation, state, current contributions, or
testbench-specific constants.

## Output Contract

Return exactly one source artifact named `phase_detector_chopper.va`.
