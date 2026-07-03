# Deadband Voltage Audit

- Gate 1: `valid_variant_needs_counting_policy`. This is a single-ended
  signed deadband-residue shaper and is functionally close to
  `143-deadband-window`; count at most one such row unless the release policy
  explicitly keeps both naming/default-parameter variants.
- Gate 2: `cadence_modeling_ready` after this revision's targeted
  EVAS/negative, Spectre, and AHDL-lint validation. The reference
  implementation computes the piecewise target first and contributes once to
  avoid branch-switched voltage contributions.
- AHDL triage: EVAS AHDL-like lint reports zero diagnostics, and Spectre
  read-in reports no task-level AHDL errors; remaining notices are global setup
  notices.
- Public contract: overridable `sigin_dead_low`/`sigin_dead_high` thresholds,
  zero output inside the window, signed excess outside the nearest threshold.
- Coverage: validation samples exercise below-window, inside-window, above-window,
  and sign-preserving residue behavior; five behavior negatives reject zero,
  missing-deadband, wrong-threshold, wrong-sign, and scaling implementations.
