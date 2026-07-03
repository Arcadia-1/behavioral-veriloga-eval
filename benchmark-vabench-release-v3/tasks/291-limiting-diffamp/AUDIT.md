# Limiting Diffamp Audit

- Gate 1: `valid_variant_needs_counting_policy`. This row is a simple centered
  hard-limiting differential amplifier. It overlaps with richer limiting
  differential-amplifier rows such as `153-limiting-differential-amplifier`;
  count it only if the release policy keeps a simpler centered-rail variant.
- Gate 2: `cadence_modeling_ready` after this revision's targeted
  EVAS/negative, Spectre, and AHDL-lint validation. The reference
  implementation computes a real target and contributes once.
- AHDL triage: EVAS AHDL-like lint reports zero diagnostics, and Spectre
  read-in reports no task-level AHDL errors; remaining notices are global setup
  notices.
- Public contract: differential gain followed by hard saturation to
  overridable lower and upper output rails.
- Coverage: validation samples exercise lower saturation, linear negative output,
  linear positive output, and upper saturation; five behavior negatives reject
  zero, missing-limit, wrong-gain, inverted-polarity, and scaling
  implementations.
