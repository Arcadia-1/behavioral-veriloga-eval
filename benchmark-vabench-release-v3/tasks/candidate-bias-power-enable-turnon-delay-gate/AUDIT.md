# Power Enable Turn-On Delay Gate Audit

- Gate 1: `independent_l1_ready` as a non-numbered materialized replacement
  candidate. This row models a reusable power-enable sequencer: sampled supply
  and bias validity, enable, power-down, and a consecutive-cycle turn-on delay
  jointly determine downstream drive enable. It is distinct from POR/UVLO rows
  and from the instantaneous supply/bias validity gate because it requires a
  stable valid interval before release. It should not be counted as an appended
  benchmark row; if accepted, upstream should assign a replacement slot inside
  the original `001`-`300` surface or keep it outside the scored denominator.
- Gate 2: `cadence_modeling_ready` for this replacement-candidate slice. Public
  prompt exposes the rail-relative validity windows, enable/power-down polarity,
  rising-clock sequencing, consecutive-cycle delay, progress monitor, and
  transition timing without leaking checker sample windows. Targeted EVAS
  verification passes gold and rejects all five negative variants. Fresh Spectre
  bridge validation passes visible and hidden gold, and hidden Spectre negatives
  reject all five variants. EVAS lint preflight reports no diagnostics for
  visible or hidden solution decks. AHDL log triage found no task-level
  `AHDLLINT-*`, `VACOMP-1116`, or AHDL compile errors; only global
  bridge/Spectre setup notices such as `VACOMP-2435` and `SPECTRE-592` appear.
- Cadence reference correspondence: Cadence behavioral-modeling guidance shows
  power-enabled flags, enable/power-down controls, supply/bias error flags, and
  additional turn-on delay before output drive is allowed. This candidate
  captures that power sequencing pattern in a pure voltage-domain DUT.
