# Max Detector Hold Audit

- Gate 1: `independent_l1_ready`. Retain as a stateful analog peak/max detector
  utility. Cadence Verilog-A course notes include max/min detector and
  sample/hold patterns as real behavioral-modeling idioms.
- Duplicate review: distinct from sample-and-hold rows because the state updates
  whenever the input exceeds the retained maximum, not only on an external clock.
- Gate 2: public prompt now uses the mandatory v3 instruction shape and exposes
  initialization, monotone hold behavior, and direct voltage-domain output.
- Validation focus: stable samples check rising updates and hold-through-falling
  behavior, with an additional monotonic held-maximum check.
