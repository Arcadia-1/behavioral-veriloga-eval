# TDC Ideal Edge Delta Audit

- Gate 1: `independent_l1_ready`. Retain as a TDC-style timing measurement
  primitive.
- Duplicate review: distinct from `133-time-diff-detector`. This row resets a
  measurement window with `samp`, updates after both input edges are observed,
  and normalizes by `fullrange`; 133 is a clocked previous-cycle detector with
  scale and output clipping.
- Gate 2: public prompt now uses the mandatory v3 instruction shape and exposes
  reset-window semantics, edge thresholds, retained output across `samp`, and
  normalized edge-delta output.
- Validation focus: stable samples cover negative and positive edge deltas across
  multiple sample windows.
