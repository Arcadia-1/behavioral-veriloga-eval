# ADC Static Linearity Monitor Audit

- Gate 1: `l2_measurement_ready` pending counting policy as a materialized
  replacement candidate. This row is a converter measurement monitor rather
  than another converter core; it samples settled ADC sweep points and
  accumulates the maximum static code error over the run. It should not be
  counted as an appended `501` benchmark row; if accepted, upstream should
  assign it to a replacement slot in the original `001`-`300` surface or mark it
  as a measurement/support L2 row.
- Gate 2: EVAS behavior-certified, with `cadence_lint_pending` until fresh AHDL
  lint/Spectre evidence is attached. Public prompt exposes the sample strobe,
  ideal-code binning, observed-code decoding, maximum-error retention, and
  metric scaling without leaking checker sample windows. Targeted local EVAS
  verification passes gold and rejects all five negative variants; Cadence
  bridge check is currently blocked by `bridge_repo_missing`.
- Cadence reference correspondence: converter verification flows commonly sweep
  input levels and reduce observed code behavior into static error metrics.
  This candidate captures that measurement pattern as a deterministic
  voltage-domain monitor.
