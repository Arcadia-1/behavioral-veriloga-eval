# Two Period Sample Delay Audit

- Gate 1: `independent_l1_ready`. Retain as an analog sample-delay utility for
  sampled-data paths.
- Duplicate review: distinct from ordinary sample-and-hold rows because it
  outputs the previous update sample rather than the current input sample.
  Distinct from multi-channel sampler/router rows because the core function is
  temporal delay, not channel selection.
- Gate 2: public prompt now uses the mandatory v3 instruction shape and exposes
  `vth`, `init`, transition time, rising-edge sampling, previous-sample output,
  and pre-valid-sample behavior.
- Validation focus: stable samples cover the initial value and multiple delayed
  update cycles; negatives cover tracking/current-sample and initialization
  errors.
