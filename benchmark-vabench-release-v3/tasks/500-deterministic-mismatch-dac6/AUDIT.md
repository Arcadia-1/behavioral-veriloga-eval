# Deterministic Mismatch DAC6 Audit

- Gate 1: `valid_variant_needs_counting_policy` as materialized replacement
  candidate. This row models deterministic element mismatch and actual-weight
  full-scale normalization, distinct from ideal binary and sub-radix DAC rows.
  It should not be counted as an appended `500` benchmark row; if accepted,
  upstream should assign it to a replacement slot in the original `001`-`300`
  surface.
- Gate 2: `cadence_modeling_ready` for this replacement-candidate slice. Public
  prompt exposes the mismatch coefficients as circuit parameters, bit order,
  normalization rule, and transition timing. Targeted EVAS verification passes
  gold and rejects all five negative variants. Fresh Spectre bridge validation
  passes visible and hidden gold, and hidden Spectre negatives reject all five
  variants. AHDL log triage found no task-level `AHDLLINT-*` or AHDL compile
  errors; only the global `VACOMP-2435` environment-variable deprecation warning
  appears.
- Cadence reference correspondence: Cadence converter modeling examples use
  weighted sums of voltage-coded decisions to build DAC behavior. This candidate
  extends that pattern with public deterministic element-weight errors rather
  than private/random mismatch.
