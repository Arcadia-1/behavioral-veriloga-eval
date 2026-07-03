# Supply Bias Validity Gate Audit

- Gate 1: `independent_l1_ready` as a non-numbered materialized replacement candidate. This
  row models reusable supply/bias validity gating for a behavioral macro: supply
  window, local ground displacement, `vss`-referenced bias validity, enable, and
  power-down jointly determine `ok` and downstream drive-enable observables. It
  is not another POR or UVLO threshold-event detector. It should not be counted
  as an appended benchmark row; if accepted, upstream should assign it to
  a replacement slot in the original `001`-`300` surface or keep it outside the
  scored denominator.
- Gate 2: `cadence_modeling_ready` for this replacement-candidate slice. Public
  prompt exposes the rail-relative supply and bias windows, enable/power-down
  polarity, output levels, and transition timing without leaking checker sample
  windows. Targeted EVAS verification passes gold and rejects all five negative
  variants. Fresh Spectre bridge validation passes visible and hidden gold, and
  hidden Spectre negatives reject all five variants. EVAS lint preflight reports
  no diagnostics for visible or hidden solution decks. AHDL log triage found no
  task-level `AHDLLINT-*`, `VACOMP-1116`, or AHDL compile errors; only global
  bridge/Spectre setup notices such as `VACOMP-2435` and `SPECTRE-592` appear.
- Cadence reference correspondence: Cadence behavioral-modeling guidance
  recommends adding supply and bias limits, shutdown controls, and automatic
  validity checks to macro models. This candidate captures that pattern as a
  voltage-domain support/control function.
