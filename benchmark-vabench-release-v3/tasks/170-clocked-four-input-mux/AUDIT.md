# Clocked Four Input Mux Audit

- Gate 1: `independent_l1_ready`. Retain as the plain clocked analog mux
  sampler baseline for sampled-data routing.
- Duplicate review: distinct from threshold-only mux rows because it latches
  only on falling clock edges. Distinct from `216-clocked-mux4-sampler`, which
  adds update/reset behavior and was handled in the digital/control review.
- Gate 2: public prompt now uses the mandatory v3 instruction shape and exposes
  full port order, select-bit order, falling-edge update, initial value, and
  held output behavior.
- Validation focus: stable samples cover all four select codes and reject wrong
  edge, wrong select order, and continuous-tracking variants.
