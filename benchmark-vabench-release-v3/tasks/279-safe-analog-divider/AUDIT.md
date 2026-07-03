# Safe Analog Divider Audit

- Gate 1: `hard_duplicate_rewrite_or_remove` / support policy candidate. This
  row is valid Verilog-A, but it should not be counted separately together with
  `150-safe-voltage-divider`; both implement a guarded analog quotient with
  sign-sensitive denominator clamping.
- Current disposition: keep as historical/support material unless upstream
  chooses it as the representative safe-divider row. This review retains 150 as
  the canonical scored representative because it already has a positive-range
  denominator parameter and a more general mixed-signal utility placement.
- Gate 2: public prompt now uses the mandatory v3 instruction shape and exposes
  the same denominator-clamp contract as 150, with this row's artifact name and
  default `min_sigdenom`.
- Validation focus: stable samples cover normal division and positive/negative
  clamp branches.
