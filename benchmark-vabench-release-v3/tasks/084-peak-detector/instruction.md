# Peak Detector

Implement `peak_detector.va` in Verilog-A.

## Interface

```verilog
module peak_detector(vin, rst, vout);
```

Inputs:

- `vin`: electrical input to measure.
- `rst`: electrical reset input using 0/0.9 V logic levels.

Outputs:

- `vout`: electrical output holding the measured peak.

## Required Behavior

Write a pure voltage-domain resettable peak detector. The model should sample
`vin` on a 500 ps timer, retain the maximum sampled value, and drive `vout`
from that retained peak.

Public parameters:

- `vth = 0.45 V`: reset threshold for `rst`.
- `tr = 500 ps`: rise/fall smoothing for `vout`.

Required observable behavior:

- Initialize the retained peak to 0 V.
- While `rst` is above `vth`, clear the retained peak to 0 V.
- While reset is inactive, update the retained peak when a sampled `vin` value
  is larger than the current peak.
- Hold the first peak, clear it on reset, and update to a larger later peak.

Use voltage contributions only. Smooth `vout` with `transition()`. Do not
generate a Spectre testbench, waveform files, checker artifacts,
transistor-level devices, current contributions, `ddt()`, or `idt()`.

## Output

Return exactly one complete Verilog-A file named `peak_detector.va`.
