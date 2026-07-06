# Power Enable Turn-On Delay Gate Audit

- Gate 1: `independent_l1_ready` as issue #109 numbered replacement row `497`.
  This row models a reusable power-enable sequencer: sampled supply
  and bias validity, enable, power-down, and a consecutive-cycle turn-on delay
  jointly determine downstream drive enable. It is distinct from POR/UVLO rows
  and from the instantaneous supply/bias validity gate because it requires a
  stable valid interval before release.
- Gate 2: `cadence_modeling_ready` for this replacement slice. Public
  prompt exposes the rail-relative validity windows, enable/power-down polarity,
  rising-clock sequencing, consecutive-cycle delay, progress monitor, and
  transition timing without leaking checker sample windows. Fresh EVAS behavior
  validation passes visible and hidden gold and rejects all five negative
  variants on both splits. Fresh Spectre bridge validation passes visible and
  hidden gold and rejects all five hidden negative variants. EVAS lint preflight
  reports no diagnostics for visible or hidden solution decks. Spectre report
  triage found no task-level `AHDLLINT-*`, `VACOMP-1116`, or AHDL compile
  errors.
- Cadence reference correspondence: Cadence behavioral-modeling guidance shows
  power-enabled flags, enable/power-down controls, supply/bias error flags, and
  additional turn-on delay before output drive is allowed. This row
  captures that power sequencing pattern in a pure voltage-domain DUT.
