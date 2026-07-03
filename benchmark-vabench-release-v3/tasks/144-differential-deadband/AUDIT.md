# Differential Deadband Audit

- Gate 1: `independent_l1_ready`. This is the symmetric-gain differential
  deadband amplifier form; `290-deadband-diffamp` remains a richer asymmetric
  low/high-gain variant.
- Gate 2: `cadence_modeling_ready` after this revision's targeted
  EVAS/negative, Spectre, and AHDL-lint validation. The reference
  implementation computes the piecewise target first and contributes once to
  avoid branch-switched voltage contributions.
- AHDL triage: EVAS AHDL-like lint reports zero diagnostics, and Spectre
  read-in reports no task-level AHDL errors; remaining notices are global setup
  notices.
- Public contract: differential input `V(sigin_p, sigin_n)`, overridable
  `dead_low`/`dead_high`, single `gain`, and leakage output level inside the
  deadband.
- Coverage: validation samples exercise negative residue, leakage region, positive
  residue, and near-window behavior; five behavior negatives reject zero,
  missing-leak, wrong-offset, single-ended, and scaling implementations.
