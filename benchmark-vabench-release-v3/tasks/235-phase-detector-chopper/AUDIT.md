# Phase Detector Chopper Audit

- Gate 1: `independent_l1_ready`. Retain as an RF/baseband chopper primitive
  that sign-modulates an input by local-oscillator polarity.
- Duplicate review: distinct from a generic analog multiplier because one input
  acts as a polarity selector, not as a continuous multiplicative operand.
  Distinct from PLL phase-detector logic rows because the output is a chopped
  analog waveform, not UP/DOWN timing pulses.
- Gate 2: public prompt now uses the mandatory v3 instruction shape and exposes
  `gain`, LO positive vs non-positive polarity behavior, and direct voltage
  output.
- Validation focus: stable samples cover both LO polarities and both RF input
  signs.
