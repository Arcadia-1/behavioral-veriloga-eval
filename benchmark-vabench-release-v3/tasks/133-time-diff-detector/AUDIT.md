# Time Diff Detector Audit

- Gate 1: `independent_l1_ready`. Retain as a clocked AMS timing primitive that
  converts edge-time difference into a bounded voltage.
- Duplicate review: distinct from `213-tdc-ideal-edge-delta`. This row publishes
  the previous acquisition cycle on the next clock edge, rearms after that
  clock, scales by `scale`, and clips to `[-vdd,+vdd]`; 213 is an immediate
  reset-window TDC-style normalized edge delta.
- Gate 2: public prompt now uses the mandatory v3 instruction shape and exposes
  thresholds, scale, clipping, one-edge-per-cycle rearm semantics, and output
  transition parameters.
- Validation focus: stable samples cover initial zero, negative clipped interval,
  and positive clipped interval; negatives cover sign, scale, and rearm errors.
