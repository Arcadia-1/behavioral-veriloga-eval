# Power Mode Supply Current Metric Audit

- Gate 1: `independent_l1_ready` as issue #109 numbered replacement row `498`. This
  row models a voltage-coded supply-current metric for macro power accounting
  across enable, power-down, operating mode, load demand, and local supply
  scaling. It is not an LDO or output-regulation task; the function is reusable
  supply-current bookkeeping in the voltage-domain vaBench surface.
- Gate 2: `cadence_modeling_ready` for this replacement slice. Public
  prompt exposes the mode-dependent baseline metric, disabled/power-down metric,
  load contribution, supply normalization, clipping, output scaling, and
  transition timing without leaking checker sample windows. Fresh EVAS behavior
  validation passes visible and hidden gold and rejects all five negative
  variants on both splits. Fresh Spectre bridge validation passes visible and
  hidden gold and rejects all five hidden negative variants. EVAS lint preflight
  reports no diagnostics for visible or hidden solution decks. Spectre report
  triage found no task-level `AHDLLINT-*`, `VACOMP-1116`, or AHDL compile
  errors.
- Cadence reference correspondence: Cadence behavioral-modeling guidance notes
  that macro supply current should reflect operating mode, shutdown behavior,
  load/output demand, and supply-voltage scaling. This row keeps that
  modeling convention while avoiding branch-current contributions.
