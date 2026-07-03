# Level Shifter Offset Audit

- Gate 1: `independent_l1_ready` with low complexity noted. Retain as a simple
  analog level-shift primitive, but do not overclaim it as a complex macro.
- Duplicate review: distinct from offset-gain amplifier rows because it applies
  only an additive level shift with unity gain and no input offset correction.
- Gate 2: public prompt now uses the mandatory v3 instruction shape and exposes
  module interface, overrideable `sigshift`, and direct `input + offset`
  voltage-domain behavior.
- Validation focus: stable samples cover positive, negative, and large input
  levels and reject missing-offset, wrong-sign, and scale variants.
