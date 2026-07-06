# Thermometer Bus Encoder Audit

- Gate 1: `independent_l1_ready` as an issue #109 re-slot. This row models a
  reusable analog-to-thermometer bus encoder/source, distinct from rows that
  summarize or decode an already-existing thermometer bus.
- Gate 2: `cadence_modeling_ready`. Public prompt exposes bus order, endpoint
  clipping, monotonic prefix behavior, output level, and transition timing
  without leaking checker sample windows. Post-re-slot validation passes EVAS
  hidden gold and rejects all five EVAS hidden negative variants. Spectre bridge
  validation passes visible and hidden gold, and visible/hidden Spectre
  negatives reject all five variants. AHDL log triage found no task-level AHDL
  compile errors; only shared setup warnings such as `VACOMP-2435` and
  `SPECTRE-592` appear.
- Cadence reference correspondence: local Cadence ASK material includes a
  Verilog-A thermometer encoded bus generator. This benchmark adapts that
  source-style pattern to a dynamic analog-input encoder so one task can
  exercise multiple thermometer codes.
