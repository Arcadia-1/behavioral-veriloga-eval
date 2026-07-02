# DC Aware ADC3bit Audit

- Gate 1: `valid_variant_needs_counting_policy` as materialized replacement
  candidate. This row is a static/combinational ADC model whose output is valid
  without a sampling clock, distinct from clocked ADC rows and thermometer-bus
  source rows. It should not be counted as an appended `498` benchmark row; if
  accepted, upstream should assign it to a replacement slot in the original
  `001`-`300` surface.
- Gate 2: EVAS behavior-certified, with `cadence_lint_pending` until fresh AHDL
  lint/Spectre evidence is attached. Public prompt exposes clipping, bin-floor
  quantization, bit order, output level, and transition timing without leaking
  checker sample windows. Targeted local EVAS verification passes gold and
  rejects all five negative variants; Cadence bridge check is currently blocked
  by `bridge_repo_missing`.
- Cadence reference correspondence: Cadence converter examples commonly model
  ideal ADC behavior by clipping or bounding the analog input, mapping it to a
  discrete code, and driving voltage-coded digital outputs. This candidate keeps
  the static conversion behavior explicit instead of adding a clocked sampling
  contract.
