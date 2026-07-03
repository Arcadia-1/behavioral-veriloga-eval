# Deadband Window Audit

- Gate 1: `valid_variant_needs_counting_policy`. This is a single-ended
  signed deadband-residue shaper and is functionally close to
  `289-deadband-voltage`; count at most one such row unless the release policy
  explicitly keeps both naming/default-parameter variants.
- Gate 2: `cadence_modeling_ready` after this revision's targeted
  EVAS/negative, Spectre, and AHDL-lint validation. The reference
  implementation computes the piecewise target first and contributes once to
  avoid branch-switched voltage contributions.
- AHDL triage: EVAS AHDL-like lint reports zero diagnostics, and Spectre
  read-in reports no task-level AHDL errors; remaining notices are global setup
  notices.
- Public contract: overridable `dead_low`/`dead_high` thresholds, zero output
  inside the window, signed residue outside the nearest threshold.
- Coverage: validation samples exercise below-window, inside-window, above-window,
  and near-window regions; five behavior negatives reject zero, pass-through,
  wrong-offset, clipping, and scaling implementations.
