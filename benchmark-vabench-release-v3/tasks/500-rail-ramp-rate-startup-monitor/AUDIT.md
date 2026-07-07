# Rail Ramp Rate Startup Monitor Audit

- Gate 1: `l2_measurement_ready` as issue #109 numbered replacement row
  `500`. This row is a startup characterization monitor for a locally supplied
  analog block rather than another generic threshold gate. It samples local rail
  movement, checks the supply window, qualifies ramp rate before the ready
  threshold, requires low-slew settling, and exposes both readiness and sampled
  slew.
- Gate 2: `cadence_modeling_ready` for this replacement slice. Public prompt
  exposes the local-rail measurement, ramp-rate window, settled-ready
  consecutive-count requirement, enable clearing, high-rail fault behavior, and
  bounded `slew_metric` without leaking checker sample windows. Fresh EVAS
  behavior validation passes visible and hidden gold and rejects all five
  negative variants on both splits. Fresh Spectre bridge validation passes
  visible and hidden gold and rejects all five hidden negative variants. EVAS
  lint preflight reports no diagnostics for visible or hidden solution decks.
  Spectre report triage found zero errors and no task-level `VACOMP-1116` or
  `AHDLLINT-*` diagnostics.
- Cadence reference correspondence: Cadence behavioral-modeling guidance
  recommends defining tests and consistency checks for supply, bias, and power
  behavior. This row captures the reusable startup qualification side of that
  guidance with local supply rails and observable voltage-coded status outputs.
