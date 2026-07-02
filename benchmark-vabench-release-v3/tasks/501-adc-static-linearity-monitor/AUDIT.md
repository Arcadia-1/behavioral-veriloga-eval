# ADC Static Linearity Monitor Audit

- Gate 1: `l2_measurement_ready` pending counting policy as a materialized
  replacement candidate. This row is a converter measurement monitor rather
  than another converter core; it samples settled ADC sweep points and
  accumulates the maximum static code error over the run. It should not be
  counted as an appended `501` benchmark row; if accepted, upstream should
  assign it to a replacement slot in the original `001`-`300` surface or mark it
  as a measurement/support L2 row.
- Gate 2: `cadence_modeling_ready` for this replacement-candidate slice. Public
  prompt exposes the sample strobe, ideal-code binning, observed-code decoding,
  maximum-error retention, and metric scaling without leaking checker sample
  windows. Targeted EVAS verification passes gold and rejects all five negative
  variants. Fresh Spectre bridge validation passes visible and hidden gold, and
  hidden Spectre negatives reject all five variants. AHDL log triage found no
  task-level `AHDLLINT-*` or AHDL compile errors; only the global
  `VACOMP-2435` environment-variable deprecation warning appears.
- Cadence reference correspondence: converter verification flows commonly sweep
  input levels and reduce observed code behavior into static error metrics.
  This candidate captures that measurement pattern as a deterministic
  voltage-domain monitor.
