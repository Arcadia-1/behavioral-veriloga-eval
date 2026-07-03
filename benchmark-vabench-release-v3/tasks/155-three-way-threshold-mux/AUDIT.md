# Three Way Threshold Mux Audit

- Gate 1: `independent_l1_ready`. Retain as a three-input differential-control
  analog routing primitive.
- Duplicate review: distinct from `130-analog-mux-threshold` because this row
  uses a differential control signal and a three-region threshold window with a
  middle selected input.
- Gate 2: public prompt now uses the mandatory v3 instruction shape and exposes
  differential control, inclusive window behavior, and the three output regions.
- Validation focus: stable samples cover below-window, inside-window, and
  above-window regions; negatives cover wrong input selection and threshold
  mistakes.
