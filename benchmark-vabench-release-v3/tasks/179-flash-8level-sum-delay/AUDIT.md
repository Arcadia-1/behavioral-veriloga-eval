# Flash 8-Level Sum Delay Audit

- Gate 1: kept as an independent flash ADC post-processing component because it combines differential threshold counting with one-cycle memory.
- Public contract: derive eight symmetric thresholds from the reference span, count the thresholds below the sampled differential input, output the normalized current count, and output the previous count on the delayed port.
- Cadence reference correspondence: the local thermometer-bus and ADC references support thresholded code generation; this benchmark adds a differential flash threshold ladder and registered one-cycle summary.
- Duplicate review: distinct from simple thermometer fraction rows because it uses differential input/reference-derived thresholds and explicitly checks current-versus-delayed output behavior.
- Evaluation note: hidden coverage should vary the differential input/reference scenario and checker expectations should be derived from saved input, reference, and clock waveforms.
