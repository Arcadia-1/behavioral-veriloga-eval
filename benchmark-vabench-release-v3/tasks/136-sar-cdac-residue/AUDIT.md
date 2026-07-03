# SAR CDAC Residue Audit

- Gate 1: `independent_l1_ready`. Retain as a scalar-port SAR CDAC residue
  update primitive for data-converter behavior.
- Duplicate review: distinct from full DAC rows because it models sampled
  residue evolution under SAR decision-control edges rather than static code to
  voltage conversion.
- Gate 2: public prompt now uses the mandatory v3 instruction shape and exposes
  sample events, reference span, control thresholds, edge directions, and CDAC
  bit weights.
- Validation focus: stable samples cover the initial sample, the S6 positive
  half-scale step, and monotone downward residue updates from S5 through S1.
