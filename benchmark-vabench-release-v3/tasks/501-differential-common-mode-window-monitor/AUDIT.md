# Differential Common Mode Window Monitor Audit

- Gate 1: `l2_measurement_ready` as issue #109 numbered replacement row
  `501`. This row is an analog-front-end input-validity monitor rather than a
  comparator or converter duplicate. It measures differential magnitude,
  computes common mode from the input pair, compares common mode against a
  reference, gates validity with enable, and exposes independent bounded
  differential and common-mode metrics.
- Gate 2: `cadence_modeling_ready` for this replacement slice. Public prompt
  exposes the differential/common-mode equations, enable gating, public window
  limits, and clipped metric scaling without leaking checker sample windows.
  Fresh EVAS behavior validation passes visible and hidden gold and rejects all
  five negative variants on both splits. Fresh Spectre bridge validation passes
  visible and hidden gold and rejects all five hidden negative variants. EVAS
  lint preflight reports no diagnostics for visible or hidden solution decks.
  Spectre report triage found zero errors and no task-level `VACOMP-1116` or
  `AHDLLINT-*` diagnostics.
- Cadence reference correspondence: Cadence behavioral-modeling guidance
  emphasizes validating model interface operating conditions with observable
  checks. This row captures that input-validity measurement pattern for a
  differential voltage-domain front end, including both differential range and
  common-mode range.
