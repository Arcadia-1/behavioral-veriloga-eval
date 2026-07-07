# Reference Settling Window Monitor Audit

- Gate 1: `l2_measurement_ready` as issue #109 numbered replacement row `496`.
  This row is a reference/bias characterization monitor rather than
  another reference generator. It measures absolute error to a target, requires
  consecutive in-window samples before declaring validity, and reports both
  error and settling progress.
- Gate 2: `cadence_modeling_ready` for this replacement slice. Public
  prompt exposes the sampled `err_metric`, tolerance window, reset behavior,
  consecutive-cycle settling requirement, progress monitor, and transition
  timing without leaking checker sample windows. Fresh EVAS behavior validation
  passes visible and hidden gold and rejects all five negative variants on both
  splits. Fresh Spectre bridge validation passes visible and hidden gold and
  rejects all five hidden negative variants. EVAS lint preflight reports no
  diagnostics for visible or hidden solution decks. Spectre report triage found
  no task-level `AHDLLINT-*`, `VACOMP-1116`, or AHDL compile errors.
- Cadence reference correspondence: Cadence behavioral-modeling guidance
  recommends defining tests and consistency checks for supply, bias, and power
  behavior. This row captures the reusable characterization side of that
  guidance for reference/bias settling.
