# Power Mode Supply Current Metric Audit

- Gate 1: `independent_l1_ready` as a non-numbered materialized replacement candidate. This
  row models a voltage-coded supply-current metric for macro power accounting
  across enable, power-down, operating mode, load demand, and local supply
  scaling. It is not an LDO or output-regulation task; the function is reusable
  supply-current bookkeeping in the voltage-domain vaBench surface. It should
  not be counted as an appended benchmark row; if accepted, upstream should
  assign it to a replacement slot in the original `001`-`300` surface or keep it
  outside the scored denominator.
- Gate 2: `cadence_modeling_ready` for this replacement-candidate slice. Public
  prompt exposes the mode-dependent baseline metric, disabled/power-down metric,
  load contribution, supply normalization, clipping, output scaling, and
  transition timing without leaking checker sample windows. Targeted EVAS
  verification passes gold and rejects all five negative variants. Fresh Spectre
  bridge validation passes visible and hidden gold, and hidden Spectre negatives
  reject all five variants. EVAS lint preflight reports no diagnostics for
  visible or hidden solution decks. AHDL log triage found no task-level
  `AHDLLINT-*`, `VACOMP-1116`, or AHDL compile errors; only global
  bridge/Spectre setup notices such as `VACOMP-2435` and `SPECTRE-592` appear.
- Cadence reference correspondence: Cadence behavioral-modeling guidance notes
  that macro supply current should reflect operating mode, shutdown behavior,
  load/output demand, and supply-voltage scaling. This candidate keeps that
  modeling convention while avoiding branch-current contributions.
