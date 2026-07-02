# Thermometer Bus Encoder Audit

- Gate 1: `valid_variant_needs_counting_policy` as materialized replacement
  candidate. This row models a reusable analog-to-thermometer bus
  encoder/source, distinct from rows that summarize or decode an already-existing
  thermometer bus. It should not be counted as an appended `497` benchmark row;
  if accepted, upstream should decide whether it replaces a thermometer support
  row, becomes a support-component benchmark, or remains outside the scored
  denominator.
- Gate 2: behavior-certified in the staging layer. Public prompt exposes bus
  order, endpoint clipping, monotonic prefix behavior, output level, and
  transition timing. Re-run Spectre/AHDL evidence after any final renumbering or
  replacement-slot edit.
- Cadence reference correspondence: local Cadence ASK material includes a
  Verilog-A thermometer encoded bus generator. This benchmark adapts that
  source-style pattern to a dynamic analog-input encoder so one task can
  exercise multiple thermometer codes.
