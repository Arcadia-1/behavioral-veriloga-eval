# Flash ADC Threshold Taps Audit

- Gate 1: kept as an independent flash ADC front-end helper because it evaluates selected threshold taps from a 31-level ladder rather than a full scalar code reconstruction.
- Public contract: on rising `clk`, compare `vin` against selected threshold indices 1, 5, 10, 15, 20, 25, and 30 across the `vrefn..vrefp` range and drive rail-coded thermometer outputs.
- Cadence reference correspondence: the local Cadence thermometer-bus article demonstrates thresholded bus generation; this task applies that modeling pattern to selected sampled flash ADC taps.
- Duplicate review: distinct from retained centered-summary and residue rows because it exposes individual selected comparator tap decisions instead of a reduced count or residue.
- Evaluation note: hidden coverage should use a different `vin` trajectory and checker expectations should be derived from saved `vin` and clock samples.
