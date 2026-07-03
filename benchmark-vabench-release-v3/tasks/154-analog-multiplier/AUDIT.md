# Analog Multiplier Audit

- Gate 1: `independent_l1_ready` with low complexity noted. Retain as a
  reusable analog arithmetic primitive.
- Duplicate review: distinct from chopper/phase-detector rows because both
  inputs are continuous analog operands and the output is their signed product,
  not sign switching by an LO rail.
- Gate 2: public prompt now uses the mandatory v3 instruction shape and exposes
  module interface, `gain`, signed product behavior, and direct voltage-domain
  output.
- Validation focus: stable samples recompute the product from observed inputs and
  reject zero, half-scale, swapped-sign, and offset-like variants.
