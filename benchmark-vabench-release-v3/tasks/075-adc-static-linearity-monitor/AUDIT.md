# ADC Static Linearity Monitor Audit

- Gate 1: `l2_measurement_ready` as an issue #109 re-slot. This row is a
  converter measurement monitor rather than another converter core; it samples
  settled ADC sweep points and accumulates the maximum static code error over
  the run.
- Gate 2: `cadence_modeling_ready`. Public prompt exposes the sample strobe,
  ideal-code binning, observed-code decoding, maximum-error retention, and
  metric scaling without leaking checker sample windows. Post-re-slot validation
  passes EVAS hidden gold and rejects all five EVAS hidden negative variants.
  Spectre bridge validation passes visible and hidden gold, and visible/hidden
  Spectre negatives reject all five variants. AHDL log triage found no
  task-level AHDL compile errors; only shared setup warnings such as
  `VACOMP-2435` and `SPECTRE-592` appear.
- Cadence reference correspondence: converter verification flows commonly sweep
  input levels and reduce observed code behavior into static error metrics.
  This candidate captures that measurement pattern as a deterministic
  voltage-domain monitor.
