# Latched Bus DAC8 Audit

- Gate 1: `valid_variant_needs_counting_policy` as materialized replacement
  candidate. This row models a parallel update-strobe DAC that samples an input
  bus on clock edges and holds the analog output between updates. That latch and
  hold behavior is distinct from purely combinational binary DAC rows. It should
  not be counted as an appended `499` benchmark row; if accepted, upstream
  should assign it to a replacement slot in the original `001`-`300` surface.
- Gate 2: `cadence_modeling_ready` for this replacement-candidate slice. Public
  prompt exposes clock edge, bit order, endpoint mapping, hold behavior, and
  transition timing without leaking checker sample windows. Targeted EVAS
  verification passes gold and rejects all five negative variants. Fresh
  Spectre bridge validation passes visible and hidden gold, and hidden Spectre
  negatives reject all five variants. AHDL log triage found no task-level
  `AHDLLINT-*` or AHDL compile errors; only the global `VACOMP-2435`
  environment-variable deprecation warning appears.
- Cadence reference correspondence: Cadence converter models commonly threshold
  voltage-coded buses and update converter state at clock/event boundaries. This
  candidate uses that modeling pattern while keeping the public contract at the
  observable latched-DAC level.
