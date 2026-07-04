# DAC7 Code Generator Audit

- Gate 1: `l2_support_component` / stimulus support. The row is useful as a
  DAC stimulus/code-source helper, but should not be overcounted as a standalone
  core circuit function unless the benchmark policy explicitly counts reusable
  source/support components.
- Duplicate review: distinct from DAC conversion rows because it generates
  voltage-coded input bits; it does not convert a code to an analog output.
- Gate 2: public prompt now uses the mandatory v3 instruction shape and exposes
  clock threshold, output levels, transition time, counter wrap, inversion, and
  bit ordering.
- Validation focus: stable samples cover several counter bits and reject bit-order,
  inversion, and update-edge errors.
