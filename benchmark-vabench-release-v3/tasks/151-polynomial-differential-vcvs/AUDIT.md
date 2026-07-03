# Polynomial Differential VCVS Audit

- Gate 1: `independent_l1_ready`. Retain as a nonlinear differential VCVS
  primitive with polynomial shaping, saturation, and common-mode centered
  outputs.
- Duplicate review: distinct from simple gain, limiting-diffamp, and ideal
  opamp rows because it exposes multiple polynomial coefficient orders and a
  half-differential saturation target.
- Gate 2: public prompt now uses the mandatory v3 instruction shape and exposes
  polynomial coefficients, common-mode parameter, saturation limit, and
  differential output mapping.
- Validation focus: stable samples cover negative, zero, positive, and saturated
  response regions and check output common-mode preservation.
