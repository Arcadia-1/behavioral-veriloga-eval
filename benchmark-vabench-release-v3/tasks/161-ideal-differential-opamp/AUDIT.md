# Ideal Differential Opamp Audit

- Gate 1: `independent_l1_ready`. Retain as the stronger differential amplifier
  primitive in this tail group.
- Duplicate review: distinct from `134-differential-buffer` because this row
  generates a fixed output common-mode and applies differential output gain;
  134 is unity pass-through support.
- Gate 2: public prompt now uses the mandatory v3 instruction shape and makes
  explicit that the fixed `4.0` gain is differential output gain, with each
  output moving symmetrically around `0.5 V`.
- Validation focus: stable samples cover multiple input polarities and verify
  output common-mode preservation.
