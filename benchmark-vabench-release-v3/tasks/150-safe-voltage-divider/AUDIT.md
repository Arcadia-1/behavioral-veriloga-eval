# Safe Voltage Divider Audit

- Gate 1: `independent_l1_ready` as the canonical safe-divider representative
  in this review. Retain this row over `279-safe-analog-divider` if the scored
  set keeps only one guarded voltage divider.
- Duplicate review: `279-safe-analog-divider` implements the same function with
  a different default clamp magnitude and artifact name. Different defaults are
  not enough for independent benchmark credit.
- Gate 2: public prompt now uses the mandatory v3 instruction shape and exposes
  `gain`, positive `min_sigdenom`, sign-sensitive denominator clamping, and
  deterministic voltage-domain quotient behavior.
- Validation focus: stable samples include unclamped and clamped denominator cases;
  negatives cover zero, wrong sign/clamp, and scaling failures.
