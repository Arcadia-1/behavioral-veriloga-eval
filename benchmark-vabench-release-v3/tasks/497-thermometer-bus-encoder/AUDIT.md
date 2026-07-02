# Thermometer Bus Encoder Audit

- Gate 1: `independent_l1_ready` candidate. This row models a reusable
  analog-to-thermometer bus encoder/source, distinct from rows that summarize or
  decode an already-existing thermometer bus.
- Gate 2: `cadence_sim_pending` until fresh Spectre/AHDL evidence is attached.
  Public prompt exposes bus order, endpoint clipping, monotonic prefix behavior,
  output level, and transition timing.
- Cadence reference correspondence: local Cadence ASK material includes a
  Verilog-A thermometer encoded bus generator. This benchmark adapts that
  source-style pattern to a dynamic analog-input encoder so one task can
  exercise multiple thermometer codes.
