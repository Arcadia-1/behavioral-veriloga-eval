# Analog Mux Threshold Audit

- Gate 1: `independent_l1_ready`. Retain as a small AMS analog-routing
  primitive. It is threshold-controlled continuous analog selection, not a pure
  digital mux.
- Duplicate review: distinct from clocked mux/sampler rows because selection
  follows the analog control threshold on both rising and falling crossings
  instead of latching only on a clock edge.
- Gate 2: public prompt now uses the mandatory v3 instruction shape and exposes
  module interface, `vth`, initial selection, both crossing directions, and
  voltage-domain output behavior without validation-internal wording.
- Validation focus: stable samples cover both selected inputs and both select
  polarities; negative variants exercise swapped inputs, missing falling update,
  averaging, and scale failures.
