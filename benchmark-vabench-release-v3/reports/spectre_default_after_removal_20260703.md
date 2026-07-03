# Spectre Default Audit After Unsupported-Row Removal

Date: 2026-07-03

Scope: hidden gold Spectre audit over the default `benchmark-vabench-release-v3/tasks/` tree after moving 54 Spectre-rejected rows to `spectre-unsupported-tasks/`.

## Summary

- tasks: `451`
- pass: `400`
- fail: `51`
- fail_behavior: `21`
- fail_spectre: `30`

## Chunks

- `WORK/spectre-default-after-removal/chunk-001-180.json`: tasks=173, pass=172, fail=1
- `WORK/spectre-default-after-removal/chunk-181-340.json`: tasks=160, pass=146, fail=14
- `WORK/spectre-default-after-removal/chunk-361-505.json`: tasks=118, pass=82, fail=36

## Failures

- `069-settling-window-detector`: `FAIL_BEHAVIOR`, 7.512s; errors=1 intervals=[(55.1, 105.1), (115.1, 150.0)] settled_seen=True reset_seen=True early_seen=False
- `301-function-clamp-window`: `FAIL_SPECTRE`, 6.054s; spectre_failed rc=2
- `302-function-deadband-map`: `FAIL_SPECTRE`, 4.650s; spectre_failed rc=2
- `303-function-piecewise-gain`: `FAIL_SPECTRE`, 4.868s; spectre_failed rc=2
- `304-function-code-normalizer`: `FAIL_SPECTRE`, 5.264s; spectre_failed rc=2
- `305-function-soft-threshold`: `FAIL_SPECTRE`, 5.909s; spectre_failed rc=2
- `321-slew-limited-voltage-follower`: `FAIL_BEHAVIOR`, 9.617s; out@45.5ns=0.4502 expected=0.7500 tol=0.0900
- `322-slew-limited-mode-stepper`: `FAIL_BEHAVIOR`, 9.435s; out@65.5ns=0.3403 expected=0.6500 tol=0.1000
- `323-slew-output-reset-recovery`: `FAIL_BEHAVIOR`, 8.999s; out@35.5ns=0.0229 expected=0.3800 tol=0.1000
- `324-slew-limited-envelope`: `FAIL_BEHAVIOR`, 7.971s; out@85.5ns=0.3000 expected=0.5500 tol=0.1000
- `325-slew-asymmetric-rise-fall`: `FAIL_BEHAVIOR`, 10.232s; out@45.5ns=0.3451 expected=0.7000 tol=0.1000
- `331-above-threshold-latch`: `FAIL_SPECTRE`, 5.520s; spectre_failed rc=2
- `332-above-window-qualifier`: `FAIL_SPECTRE`, 5.248s; spectre_failed rc=2
- `333-last-crossing-period-meter`: `FAIL_SPECTRE`, 5.588s; spectre_failed rc=2
- `334-last-crossing-edge-age`: `FAIL_SPECTRE`, 4.602s; spectre_failed rc=2
- `381-file-fseek-offset-reader`: `FAIL_BEHAVIOR`, 9.606s; metric@0ns=0.0000 expected=0.9000 tol=0.0800
- `383-file-rewind-second-pass`: `FAIL_BEHAVIOR`, 8.423s; metric@0ns=0.0000 expected=0.9000 tol=0.0800
- `384-file-fopen-mode-selector`: `FAIL_BEHAVIOR`, 8.197s; metric@0ns=0.0000 expected=0.9000 tol=0.0800
- `386-table-model-clamped-transfer`: `FAIL_BEHAVIOR`, 7.587s; out@49.6502ns=-0.2722 expected=0.0000 tol=0.0800
- `388-table-model-dac-code-map`: `FAIL_BEHAVIOR`, 7.381s; out@450.174ns=1.0200 expected=0.9000 tol=0.0800
- `389-table-model-temperature-profile`: `FAIL_BEHAVIOR`, 8.331s; metric@350.133ns=0.4722 expected=0.5556 tol=0.0800
- `390-table-model-piecewise-calibrator`: `FAIL_BEHAVIOR`, 7.826s; out@450.174ns=1.0250 expected=0.9000 tol=0.0800
- `391-rdist-exponential-jitter`: `FAIL_BEHAVIOR`, 8.553s; metric@50.8369ns=5.0691 expected=3.7943 tol=0.0500
- `392-rdist-poisson-count-noise`: `FAIL_BEHAVIOR`, 7.403s; metric@50.8369ns=0.0000 expected=3.0000 tol=0.0500
- `393-rdist-normal-offset-dither`: `FAIL_BEHAVIOR`, 8.117s; metric@50.8369ns=-0.0111 expected=0.0113 tol=0.0080
- `396-rdist-erlang-latency`: `FAIL_BEHAVIOR`, 8.407s; metric@50.8369ns=1.3056 expected=1.0851 tol=0.0300
- `404-vector-part-select-window`: `FAIL_BEHAVIOR`, 9.172s; out@50.9587ns=0.0000 expected=0.9000 tol=0.0500
- `405-vector-concat-code-build`: `FAIL_BEHAVIOR`, 9.180s; metric@50.8369ns=2.0000 expected=8.0000 tol=0.0500
- `426-string-sformat-mode-tag`: `FAIL_SPECTRE`, 4.724s; spectre_failed rc=2
- `428-string-mode-tagged-log`: `FAIL_SPECTRE`, 4.443s; spectre_failed rc=2
- `429-string-config-label-select`: `FAIL_SPECTRE`, 5.077s; spectre_failed rc=2
- `435-ddt-voltage-derivative-source`: `FAIL_SPECTRE`, 4.582s; spectre_failed rc=2
- `436-idt-voltage-integrator-source`: `FAIL_SPECTRE`, 4.931s; spectre_failed rc=2
- `437-laplace-nd-lowpass-filter`: `FAIL_SPECTRE`, 5.174s; spectre_failed rc=2
- `438-laplace-np-pole-filter`: `FAIL_SPECTRE`, 4.999s; spectre_failed rc=2
- `439-laplace-zd-zero-den-filter`: `FAIL_SPECTRE`, 5.446s; spectre_failed rc=2
- `440-laplace-zp-zero-pole-filter`: `FAIL_SPECTRE`, 5.561s; spectre_failed rc=2
- `441-zi-nd-discrete-filter`: `FAIL_SPECTRE`, 4.790s; spectre_failed rc=2
- `442-zi-np-discrete-filter`: `FAIL_SPECTRE`, 4.915s; spectre_failed rc=2
- `443-zi-zd-discrete-filter`: `FAIL_SPECTRE`, 4.832s; spectre_failed rc=2
- `444-zi-zp-discrete-filter`: `FAIL_SPECTRE`, 5.239s; spectre_failed rc=2
- `457-nested-function-pipeline`: `FAIL_SPECTRE`, 5.311s; spectre_failed rc=2
- `465-port-connected-output-enable`: `FAIL_SPECTRE`, 5.785s; spectre_failed rc=2
- `469-current-contribution-conductance`: `FAIL_SPECTRE`, 8.473s; spectre_failed rc=2
- `471-indirect-branch-null-balance`: `FAIL_SPECTRE`, 5.537s; spectre_failed rc=2
- `472-indirect-branch-ddt-balance`: `FAIL_SPECTRE`, 5.967s; spectre_failed rc=1
- `480-mfactor-system-function-gain`: `FAIL_SPECTRE`, 5.673s; spectre_failed rc=2
- `486-rf-source-info-registration`: `FAIL_SPECTRE`, 4.707s; spectre_failed rc=2
- `491-kcl-capacitor-ddt-current`: `FAIL_SPECTRE`, 7.765s; spectre_failed rc=2
- `492-kcl-inductor-idt-voltage`: `FAIL_BEHAVIOR`, 8.137s; p@21ns=-5.077e-25 expected=5.000e-25 tol=2.500e-25 p@40ns=-1.951e-23 expected=1.950e-23 tol=5.850e-25 p@80ns=-5.951e-23 expected=5.950e-23 tol=1.785e-24 p@100ns=-4.050e-23 expected=4.050e-23 tol=1.215e-24
- `494-continuous-zi-nd-filter`: `FAIL_BEHAVIOR`, 8.742s; out@30ns=0.5 expected=0.08 out@40ns=1.125 expected=0.6 out@50ns=1.281 expected=1.15 out@100ns=0.2083 expected=0.483

## Slow Passing Rows Over 20s

- `061-bus-splitter-256-to-16x16`: 33.137s
- `062-bus-combiner-16x16-to-256`: 30.279s
- `097-cppll-tracking-reacquire-timer`: 22.587s

## Top Wall Times

- `061-bus-splitter-256-to-16x16`: `PASS`, 33.137s
- `062-bus-combiner-16x16-to-256`: `PASS`, 30.279s
- `097-cppll-tracking-reacquire-timer`: `PASS`, 22.587s
- `050-bin-to-thermometer-decoder-8b`: `PASS`, 19.639s
- `287-gain-extraction-flow`: `PASS`, 19.317s
- `283-weighted-sar-adc-dac-loop`: `PASS`, 17.268s
- `111-clocked-sine-source`: `PASS`, 16.606s
- `505-fractional-n-divider-accumulator-flow`: `PASS`, 15.395s
- `307-case-priority-status-decoder`: `PASS`, 13.203s
- `059-config-latch-128b-static-enable`: `PASS`, 13.170s
- `090-adpll-ratio-hop-timer`: `PASS`, 12.628s
- `269-trim-ctrl-5bit`: `PASS`, 12.393s
- `093-bbpd-data-edge-alignment`: `PASS`, 12.042s
- `483-cds-violation-threshold-assert`: `PASS`, 11.919s
- `116-clocked-comparator-reset-low`: `PASS`, 11.851s
- `314-for-loop-windowed-peak`: `PASS`, 11.764s
- `431-hierarchy-support-artifact-staging`: `PASS`, 11.656s
- `080-acquisition-limited-sample-and-hold`: `PASS`, 11.468s
- `504-charge-pump-pfd-state-machine`: `PASS`, 11.379s
- `271-coarse-qtz-3bit-residue`: `PASS`, 11.369s
