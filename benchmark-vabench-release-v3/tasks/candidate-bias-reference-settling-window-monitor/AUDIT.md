# Reference Settling Window Monitor Audit

- Gate 1: `l2_measurement_ready` as a non-numbered materialized replacement
  candidate. This row is a reference/bias characterization monitor rather than
  another reference generator. It measures absolute error to a target, requires
  consecutive in-window samples before declaring validity, and reports both
  error and settling progress. It should not be counted as an appended benchmark
  row; if accepted, upstream should assign a replacement slot inside the
  original `001`-`300` surface or keep it outside the scored denominator.
- Gate 2: `cadence_modeling_ready` for this replacement-candidate slice. Public
  prompt exposes the sampled `err_metric`, tolerance window, reset behavior,
  consecutive-cycle settling requirement, progress monitor, and transition
  timing without leaking checker sample windows. Targeted EVAS verification
  passes gold and rejects all five negative variants. Fresh Spectre bridge
  validation passes visible and hidden gold, and hidden Spectre negatives reject
  all five variants. EVAS lint preflight reports no diagnostics for visible or
  hidden solution decks. AHDL log triage found no task-level `AHDLLINT-*`,
  `VACOMP-1116`, or AHDL compile errors; only global bridge/Spectre setup
  notices such as `VACOMP-2435` and `SPECTRE-592` appear.
- Cadence reference correspondence: Cadence behavioral-modeling guidance
  recommends defining tests and consistency checks for supply, bias, and power
  behavior. This candidate captures the reusable characterization side of that
  guidance for reference/bias settling.
