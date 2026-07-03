# Max Detector Hold

## Task Contract

Implement a voltage-domain maximum detector with held peak output.

- Form: `dut`
- Level: `L1`
- Category: mixed-signal stateful analog utility
- Target artifact: `max_detector_hold.va`

## Form-Specific Requirements

Return only the DUT source file. Do not generate a simulation harness, validation script, waveform
postprocessor, or companion support module.

## Public Verilog-A Interface

`max_detector_hold.va` must declare:

```verilog
module max_detector_hold(vin, vout);
input vin;
output vout;
electrical vin, vout;
```

## Public Parameter Contract

This task has no public Verilog-A parameters.

## Required Behavior

Initialize the held maximum to the input voltage at the start of transient
simulation. Whenever `V(vin)` rises above the held maximum, update the held
maximum to the new input value. When `V(vin)` falls or stays below the held
maximum, keep the previous maximum.

Continuously drive `vout` with the held maximum.

## Modeling Constraints

Use deterministic voltage-domain state. Do not reset the maximum after
initialization, track the input downward, add smoothing, or hard-code testbench
sample times.

## Output Contract

Return exactly one source artifact named `max_detector_hold.va`.
