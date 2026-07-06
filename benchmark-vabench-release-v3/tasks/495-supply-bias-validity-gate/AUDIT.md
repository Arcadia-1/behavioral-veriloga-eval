# Supply Bias Validity Gate Audit

- Gate 1: `independent_l1_ready` as issue #109 numbered replacement row `495`. This
  row models reusable supply/bias validity gating for a behavioral macro: supply
  window, local ground displacement, `vss`-referenced bias validity, enable, and
  power-down jointly determine `ok` and downstream drive-enable observables. It
  is not another POR or UVLO threshold-event detector.
- Gate 2: `cadence_modeling_ready` for this replacement slice. Public
  prompt exposes the rail-relative supply and bias windows, enable/power-down
  polarity, output levels, and transition timing without leaking checker sample
  windows. Fresh EVAS behavior validation passes visible and hidden gold and
  rejects all five negative variants on both splits. Fresh Spectre bridge
  validation passes visible and hidden gold and rejects all five hidden
  negative variants. EVAS lint preflight reports no diagnostics for visible or
  hidden solution decks. Spectre report triage found no task-level
  `AHDLLINT-*`, `VACOMP-1116`, or AHDL compile errors.
- Cadence reference correspondence: Cadence behavioral-modeling guidance
  recommends adding supply and bias limits, shutdown controls, and automatic
  validity checks to macro models. This row captures that pattern as a
  voltage-domain support/control function.
