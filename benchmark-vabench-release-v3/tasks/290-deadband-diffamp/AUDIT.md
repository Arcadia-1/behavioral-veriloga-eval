# Deadband Diffamp Audit

- Gate 1: `independent_l1_ready`. This is the asymmetric-gain differential
  deadband amplifier form and is meaningfully distinct from
  `144-differential-deadband`, which has one shared gain for both sides.
- Gate 2: `cadence_modeling_ready` after this revision's targeted
  EVAS/negative, Spectre, and AHDL-lint validation. The reference
  implementation computes the piecewise target first and contributes once to
  avoid branch-switched voltage contributions.
- AHDL triage: EVAS AHDL-like lint reports zero diagnostics, and Spectre
  read-in reports no task-level AHDL errors; remaining notices are global setup
  notices.
- Public contract: differential input `V(sigin_p, sigin_n)`, leakage output in
  the deadband, independent low-side and high-side gains outside the thresholds.
- Coverage: validation samples exercise low-side residue, leakage region,
  high-side residue, and asymmetric gain behavior; five behavior negatives
  reject zero, missing-leak, symmetric-gain, inverted-polarity, and scaling
  implementations.
