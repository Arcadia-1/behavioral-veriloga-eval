# Two Channel Sample Demux Audit

- Gate 1: `independent_l1_ready`. Retain as a sampled-data analog routing
  primitive with two independent clock domains selecting a shared output.
- Duplicate review: distinct from `170-clocked-four-input-mux` because each
  source has its own sampling clock instead of a select code latched by one
  clock. Distinct from `175-four-channel-edge-sampler` because it routes two
  inputs to one output instead of sampling all lanes in parallel.
- Gate 2: public prompt now uses the mandatory v3 instruction shape and exposes
  port order, `vth`, rising-edge behavior for both clocks, initial output, and
  hold semantics.
- Validation focus: stable samples cover both clock domains and multiple routed
  sample updates.
