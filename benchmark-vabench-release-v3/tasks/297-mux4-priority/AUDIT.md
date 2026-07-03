# Source Mux4 Priority Audit

- Scenario: Implement a four-channel analog mux. A 2-bit select chooses IN0, IN1, IN2, or IN3 and forwards that voltage to OUT.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.

## Digital/Control/Logic Closeout Review

- Gate 1 status: `hard_duplicate_rewrite_or_remove`.
- Rationale: this is a simple 4:1 mux behavior and overlaps with the existing
  mux/selector family. It does not add reset, latch, update qualification,
  glitch-free handoff, or analog-facing control semantics.
- Counting recommendation: keep at most one simple mux row; prefer the stronger
  update-qualified mux/control variants for core counting.
