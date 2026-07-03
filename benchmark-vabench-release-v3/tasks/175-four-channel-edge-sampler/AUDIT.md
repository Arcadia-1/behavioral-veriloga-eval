# Four Channel Edge Sampler Audit

- Gate 1: `independent_l1_ready`. Retain as a multi-lane analog sample bank for
  converter/readout support.
- Duplicate review: distinct from single-channel sample-and-hold rows and from
  `170-clocked-four-input-mux`; this row simultaneously samples four lanes on a
  shared edge rather than selecting one input.
- Gate 2: public prompt now uses the mandatory v3 instruction shape and exposes
  `direction`, `vdd/2` threshold, output transition parameters, initialization,
  simultaneous sampling, and channel order.
- Validation focus: stable samples cover all four lanes across multiple sampling
  edges and reject tracking, wrong-edge, and channel-swap variants.
