# Reference Flash 8-Level Decoder Audit

- Gate 1: kept as an independent flash sub-ADC backend because it combines thermometer count normalization with centered residue generation.
- Public contract: count eight thresholded thermometer taps on rising `clks`, output the normalized count, and compute residue from the sampled input minus the mid-code reference correction.
- Cadence reference correspondence: the local ADC reference supports code generation/quantization patterns; this task adds the residue path used by sub-ADC and pipeline/flash backend models.
- Duplicate review: stronger than simple thermometer fraction rows because it exposes both decoded code and analog residue, so it is not just a tap-count variant.
- Evaluation note: hidden coverage should vary both thermometer count and `vin`; checker expectations should be derived from saved taps, input, and clock samples.
