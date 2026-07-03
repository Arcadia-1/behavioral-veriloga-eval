# Soft Voltage Clamp Audit

- Gate 1: `independent_l1_ready`. This row models an exponential soft clamp and
  is distinct from hard clamp/limiter rows because it preserves monotonic,
  continuous soft limiting toward asymptotes.
- Gate 2: `cadence_modeling_ready` after this revision's targeted
  EVAS/negative, Spectre, and AHDL-lint validation. The prompt now describes
  the same 0.0 V and 0.4 V knee points, 0.2 V softness span, and -0.2 V /
  0.6 V asymptotes used by the reference implementation and checker.
- AHDL triage: EVAS AHDL-like lint reports zero diagnostics, and Spectre
  read-in reports no task-level AHDL errors; remaining notices are global setup
  notices.
- Public contract: pass-through in the central region, exponential lower and
  upper soft limiting outside the knees, no hard clipping at the asymptotes.
- Coverage: validation samples exercise lower soft limit, pass-through, upper soft
  limit, and near-upper-knee behavior; five behavior negatives reject zero,
  hard-clamp, wrong-knee, wrong-softness, and scaling implementations.
