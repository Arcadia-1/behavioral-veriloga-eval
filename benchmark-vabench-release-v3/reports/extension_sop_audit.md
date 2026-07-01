# v3 Extension SOP Audit

Date: 2026-07-02

## Summary

- Audited extension tasks: **194**
- SOP-ready tasks: **154**
- Tasks with executable visible+hidden SCS evidence: **194**
- Tasks with behavior checker evidence: **154**
- Tasks with distinct visible/hidden SCS stimuli: **194**
- Tasks with identical visible/hidden SCS stimuli: **0**
- SOP-ready tasks with identical visible/hidden SCS stimuli: **0**
- Staged tasks with identical visible/hidden SCS stimuli: **0**

## Issue Counts

- `checker_syntax_only_no_behavior_score`: 40

## Warning Counts

- `candidate_tier_not_score_ready`: 194

## Range Summary

| Range | Description | Tasks | Ready | Executable Tests | Behavior Eval | Distinct V/H | Top Issues |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| `301-340` | language-semantics voltage-domain candidates | 40 | 40 | 40 | 40 | 40 |  |
| `341-360` | AMS mixed-signal candidates | 20 | 19 | 20 | 19 | 20 | `checker_syntax_only_no_behavior_score`: 1 |
| `361-372` | noise and analysis candidates | 12 | 12 | 12 | 12 | 12 |  |
| `373-434` | task/file/table/random/hierarchy syntax candidates | 62 | 55 | 62 | 55 | 62 | `checker_syntax_only_no_behavior_score`: 7 |
| `435-458` | manual syntax-completion candidates | 24 | 9 | 24 | 9 | 24 | `checker_syntax_only_no_behavior_score`: 15 |
| `459-470` | course-material gap-fill candidates | 12 | 8 | 12 | 8 | 12 | `checker_syntax_only_no_behavior_score`: 4 |
| `471-494` | LRM KCL/continuous-time gap-fill candidates | 24 | 11 | 24 | 11 | 24 | `checker_syntax_only_no_behavior_score`: 13 |

## Highest Severity Finding

Tasks 301-494 are extension candidates, not SOP-ready benchmark tasks. They mostly provide syntax-focused reference artifacts plus skeleton visible/hidden Spectre decks. Under the SOP, they need concrete public behavior prompts, executable visible smoke tests, hidden formal tests, and behavior-checking negative evidence before promotion.

## Per-Task Rows

| Task | Tier | Ready | Issues |
| --- | --- | --- | --- |
| `301-function-clamp-window` | `syntax-extension-candidate` | True | - |
| `302-function-deadband-map` | `syntax-extension-candidate` | True | - |
| `303-function-piecewise-gain` | `syntax-extension-candidate` | True | - |
| `304-function-code-normalizer` | `syntax-extension-candidate` | True | - |
| `305-function-soft-threshold` | `syntax-extension-candidate` | True | - |
| `306-case-mode-gain-selector` | `syntax-extension-candidate` | True | - |
| `307-case-priority-status-decoder` | `syntax-extension-candidate` | True | - |
| `308-case-quantized-output-level` | `syntax-extension-candidate` | True | - |
| `309-case-clocked-range-bucket` | `syntax-extension-candidate` | True | - |
| `310-case-resettable-state-decoder` | `syntax-extension-candidate` | True | - |
| `311-for-loop-running-average` | `syntax-extension-candidate` | True | - |
| `312-for-loop-thermometer-count` | `syntax-extension-candidate` | True | - |
| `313-for-loop-weighted-accumulator` | `syntax-extension-candidate` | True | - |
| `314-for-loop-windowed-peak` | `syntax-extension-candidate` | True | - |
| `315-for-loop-code-popcount` | `syntax-extension-candidate` | True | - |
| `316-final-step-edge-counter-file` | `syntax-extension-candidate` | True | - |
| `317-final-step-average-metric-file` | `syntax-extension-candidate` | True | - |
| `318-final-step-max-observer-file` | `syntax-extension-candidate` | True | - |
| `319-display-strobe-event-logger` | `syntax-extension-candidate` | True | - |
| `320-file-io-sampled-metric-writer` | `syntax-extension-candidate` | True | - |
| `321-slew-limited-voltage-follower` | `syntax-extension-candidate` | True | - |
| `322-slew-limited-mode-stepper` | `syntax-extension-candidate` | True | - |
| `323-slew-output-reset-recovery` | `syntax-extension-candidate` | True | - |
| `324-slew-limited-envelope` | `syntax-extension-candidate` | True | - |
| `325-slew-asymmetric-rise-fall` | `syntax-extension-candidate` | True | - |
| `326-idtmod-phase-accumulator` | `syntax-extension-candidate` | True | - |
| `327-idtmod-wrapped-ramp-source` | `syntax-extension-candidate` | True | - |
| `328-idtmod-frequency-control` | `syntax-extension-candidate` | True | - |
| `329-idtmod-modulo-phase-marker` | `syntax-extension-candidate` | True | - |
| `330-idtmod-clock-phase-meter` | `syntax-extension-candidate` | True | - |
| `331-above-threshold-latch` | `syntax-extension-candidate` | True | - |
| `332-above-window-qualifier` | `syntax-extension-candidate` | True | - |
| `333-last-crossing-period-meter` | `syntax-extension-candidate` | True | - |
| `334-last-crossing-edge-age` | `syntax-extension-candidate` | True | - |
| `335-above-resettable-peak-marker` | `syntax-extension-candidate` | True | - |
| `336-directive-configurable-threshold` | `syntax-extension-candidate` | True | - |
| `337-parameter-range-limited-gain` | `syntax-extension-candidate` | True | - |
| `338-math-trig-envelope-detector` | `syntax-extension-candidate` | True | - |
| `339-random-seeded-dither-source` | `syntax-extension-candidate` | True | - |
| `340-bound-step-clock-guard` | `syntax-extension-candidate` | True | - |
| `341-wreal-gain-pass-through` | `ams-mixed-signal-candidate` | True | - |
| `342-wreal-two-input-summer` | `ams-mixed-signal-candidate` | True | - |
| `343-wreal-threshold-flag` | `ams-mixed-signal-candidate` | True | - |
| `344-wreal-clamped-mux` | `ams-mixed-signal-candidate` | True | - |
| `345-wreal-scale-offset` | `ams-mixed-signal-candidate` | True | - |
| `346-logic-assign-inverter` | `ams-mixed-signal-candidate` | True | - |
| `347-logic-assign-and-or` | `ams-mixed-signal-candidate` | True | - |
| `348-logic-assign-xor-flag` | `ams-mixed-signal-candidate` | True | - |
| `349-logic-assign-priority-mux` | `ams-mixed-signal-candidate` | True | - |
| `350-logic-assign-reduction` | `ams-mixed-signal-candidate` | True | - |
| `351-always-posedged-dff` | `ams-mixed-signal-candidate` | True | - |
| `352-always-negedge-sampler` | `ams-mixed-signal-candidate` | True | - |
| `353-always-resettable-toggle` | `ams-mixed-signal-candidate` | False | `checker_syntax_only_no_behavior_score` |
| `354-always-counter-two-bit` | `ams-mixed-signal-candidate` | True | - |
| `355-always-enable-hold` | `ams-mixed-signal-candidate` | True | - |
| `356-mixed-logic-enable-voltage-driver` | `ams-mixed-signal-candidate` | True | - |
| `357-mixed-wreal-to-electrical-buffer` | `ams-mixed-signal-candidate` | True | - |
| `358-mixed-electrical-threshold-logic-flag` | `ams-mixed-signal-candidate` | True | - |
| `359-mixed-logic-clocked-voltage-sampler` | `ams-mixed-signal-candidate` | True | - |
| `360-mixed-wreal-logic-select-driver` | `ams-mixed-signal-candidate` | True | - |
| `361-white-noise-voltage-source` | `noise-analysis-candidate` | True | - |
| `362-white-noise-gated-source` | `noise-analysis-candidate` | True | - |
| `363-flicker-noise-voltage-source` | `noise-analysis-candidate` | True | - |
| `364-flicker-noise-corner-selector` | `noise-analysis-candidate` | True | - |
| `365-noise-table-voltage-shaper` | `noise-analysis-candidate` | True | - |
| `366-noise-table-gated-shaper` | `noise-analysis-candidate` | True | - |
| `367-analysis-dependent-dc-tran-mode` | `noise-analysis-candidate` | True | - |
| `368-analysis-dependent-noise-enable` | `noise-analysis-candidate` | True | - |
| `369-ac-stim-small-signal-source` | `noise-analysis-candidate` | True | - |
| `370-ac-stim-phase-selector` | `noise-analysis-candidate` | True | - |
| `371-combined-white-flicker-noise` | `noise-analysis-candidate` | True | - |
| `372-analysis-aware-noise-metric` | `noise-analysis-candidate` | True | - |
| `373-task-output-limiter` | `syntax-extension-candidate` | True | - |
| `374-task-dual-output-update` | `syntax-extension-candidate` | True | - |
| `375-task-event-counter-service` | `syntax-extension-candidate` | True | - |
| `376-task-reset-sequencer` | `syntax-extension-candidate` | True | - |
| `377-task-stateful-threshold-update` | `syntax-extension-candidate` | True | - |
| `378-task-metric-normalizer` | `syntax-extension-candidate` | True | - |
| `379-file-fgets-config-loader` | `syntax-extension-candidate` | True | - |
| `380-file-feof-line-counter` | `syntax-extension-candidate` | True | - |
| `381-file-fseek-offset-reader` | `syntax-extension-candidate` | True | - |
| `382-file-ftell-position-meter` | `syntax-extension-candidate` | True | - |
| `383-file-rewind-second-pass` | `syntax-extension-candidate` | True | - |
| `384-file-fopen-mode-selector` | `syntax-extension-candidate` | True | - |
| `385-table-model-linear-gain` | `syntax-extension-candidate` | True | - |
| `386-table-model-clamped-transfer` | `syntax-extension-candidate` | True | - |
| `387-table-model-threshold-map` | `syntax-extension-candidate` | True | - |
| `388-table-model-dac-code-map` | `syntax-extension-candidate` | True | - |
| `389-table-model-temperature-profile` | `syntax-extension-candidate` | True | - |
| `390-table-model-piecewise-calibrator` | `syntax-extension-candidate` | True | - |
| `391-rdist-exponential-jitter` | `syntax-extension-candidate` | True | - |
| `392-rdist-poisson-count-noise` | `syntax-extension-candidate` | True | - |
| `393-rdist-normal-offset-dither` | `syntax-extension-candidate` | True | - |
| `394-rdist-chi-square-energy` | `syntax-extension-candidate` | True | - |
| `395-rdist-t-tail-dither` | `syntax-extension-candidate` | True | - |
| `396-rdist-erlang-latency` | `syntax-extension-candidate` | True | - |
| `397-hierarchy-gain-child` | `syntax-extension-candidate` | True | - |
| `398-hierarchy-two-stage-chain` | `syntax-extension-candidate` | True | - |
| `399-hierarchy-parameter-override` | `syntax-extension-candidate` | True | - |
| `400-hierarchy-named-port-map` | `syntax-extension-candidate` | True | - |
| `401-hierarchy-ordered-port-map` | `syntax-extension-candidate` | True | - |
| `402-hierarchy-shared-threshold-child` | `syntax-extension-candidate` | True | - |
| `403-vector-bit-select-flag` | `syntax-extension-candidate` | True | - |
| `404-vector-part-select-window` | `syntax-extension-candidate` | True | - |
| `405-vector-concat-code-build` | `syntax-extension-candidate` | True | - |
| `406-vector-replication-mask` | `syntax-extension-candidate` | True | - |
| `407-vector-reduction-parity` | `syntax-extension-candidate` | True | - |
| `408-vector-shift-and-mask-decoder` | `syntax-extension-candidate` | True | - |
| `409-macro-functionlike-clamp` | `syntax-extension-candidate` | True | - |
| `410-macro-ifdef-gain-select` | `syntax-extension-candidate` | False | `checker_syntax_only_no_behavior_score` |
| `411-escaped-identifier-state` | `syntax-extension-candidate` | True | - |
| `412-initial-final-step-lifecycle` | `syntax-extension-candidate` | True | - |
| `413-while-loop-array-sum` | `syntax-extension-candidate` | True | - |
| `414-parameter-range-real-control` | `syntax-extension-candidate` | True | - |
| `415-logic-vector-assign-slice` | `ams-mixed-signal-candidate` | False | `checker_syntax_only_no_behavior_score` |
| `416-logic-vector-reduction-flag` | `ams-mixed-signal-candidate` | False | `checker_syntax_only_no_behavior_score` |
| `417-always-async-reset-counter` | `ams-mixed-signal-candidate` | False | `checker_syntax_only_no_behavior_score` |
| `418-always-enable-saturating-counter` | `ams-mixed-signal-candidate` | False | `checker_syntax_only_no_behavior_score` |
| `419-wreal-logic-threshold-bridge` | `ams-mixed-signal-candidate` | True | - |
| `420-mixed-analog-digital-mode-latch` | `ams-mixed-signal-candidate` | True | - |
| `421-task-local-variable-transform` | `syntax-extension-candidate` | True | - |
| `422-file-fscanf-table-stimulus` | `syntax-extension-candidate` | True | - |
| `423-file-profile-replay-controller` | `syntax-extension-candidate` | True | - |
| `424-file-fscanf-multi-column-profile` | `syntax-extension-candidate` | True | - |
| `425-string-swrite-label-builder` | `syntax-extension-candidate` | True | - |
| `426-string-sformat-mode-tag` | `syntax-extension-candidate` | True | - |
| `427-string-formatted-metric-line` | `syntax-extension-candidate` | True | - |
| `428-string-mode-tagged-log` | `syntax-extension-candidate` | True | - |
| `429-string-config-label-select` | `syntax-extension-candidate` | True | - |
| `430-rdist-seed-reproducibility` | `syntax-extension-candidate` | True | - |
| `431-hierarchy-support-artifact-staging` | `syntax-extension-candidate` | False | `checker_syntax_only_no_behavior_score` |
| `432-hierarchy-nested-parameter-chain` | `syntax-extension-candidate` | False | `checker_syntax_only_no_behavior_score` |
| `433-preprocessor-ifndef-elsif-undef` | `syntax-extension-candidate` | True | - |
| `434-repeat-loop-accumulator` | `syntax-extension-candidate` | True | - |
| `435-ddt-voltage-derivative-source` | `syntax-extension-candidate` | False | `checker_syntax_only_no_behavior_score` |
| `436-idt-voltage-integrator-source` | `syntax-extension-candidate` | False | `checker_syntax_only_no_behavior_score` |
| `437-laplace-nd-lowpass-filter` | `syntax-extension-candidate` | False | `checker_syntax_only_no_behavior_score` |
| `438-laplace-np-pole-filter` | `syntax-extension-candidate` | False | `checker_syntax_only_no_behavior_score` |
| `439-laplace-zd-zero-den-filter` | `syntax-extension-candidate` | False | `checker_syntax_only_no_behavior_score` |
| `440-laplace-zp-zero-pole-filter` | `syntax-extension-candidate` | False | `checker_syntax_only_no_behavior_score` |
| `441-zi-nd-discrete-filter` | `syntax-extension-candidate` | False | `checker_syntax_only_no_behavior_score` |
| `442-zi-np-discrete-filter` | `syntax-extension-candidate` | False | `checker_syntax_only_no_behavior_score` |
| `443-zi-zd-discrete-filter` | `syntax-extension-candidate` | False | `checker_syntax_only_no_behavior_score` |
| `444-zi-zp-discrete-filter` | `syntax-extension-candidate` | False | `checker_syntax_only_no_behavior_score` |
| `445-limexp-soft-exponential` | `syntax-extension-candidate` | True | - |
| `446-fstrobe-file-line-writer` | `syntax-extension-candidate` | True | - |
| `447-display-warning-debug-log` | `syntax-extension-candidate` | True | - |
| `448-rdist-uniform-seeded-dither` | `syntax-extension-candidate` | True | - |
| `449-generate-genvar-replicated-stage` | `syntax-extension-candidate` | False | `checker_syntax_only_no_behavior_score` |
| `450-custom-nature-discipline-voltage` | `syntax-extension-candidate` | True | - |
| `451-connectmodule-electrical-bridge` | `syntax-extension-candidate` | False | `checker_syntax_only_no_behavior_score` |
| `452-connectrules-electrical-map` | `syntax-extension-candidate` | False | `checker_syntax_only_no_behavior_score` |
| `453-specify-specparam-delay` | `syntax-extension-candidate` | False | `checker_syntax_only_no_behavior_score` |
| `454-multidimensional-array-state` | `syntax-extension-candidate` | True | - |
| `455-packed-logic-bus-slice` | `syntax-extension-candidate` | False | `checker_syntax_only_no_behavior_score` |
| `456-event-or-cross-timer` | `syntax-extension-candidate` | True | - |
| `457-nested-function-pipeline` | `syntax-extension-candidate` | True | - |
| `458-recursive-function-candidate` | `syntax-extension-candidate` | True | - |
| `459-do-while-loop-accumulator` | `syntax-extension-candidate` | True | - |
| `460-analog-initial-block-state` | `syntax-extension-candidate` | True | - |
| `461-vt-thermal-voltage-source` | `syntax-extension-candidate` | True | - |
| `462-vt-temperature-argument` | `syntax-extension-candidate` | True | - |
| `463-discontinuity-event-announcement` | `syntax-extension-candidate` | True | - |
| `464-param-given-gain-select` | `syntax-extension-candidate` | False | `checker_syntax_only_no_behavior_score` |
| `465-port-connected-output-enable` | `syntax-extension-candidate` | True | - |
| `466-temperature-environment-metric` | `syntax-extension-candidate` | True | - |
| `467-simparam-query-tnom` | `syntax-extension-candidate` | True | - |
| `468-branch-declaration-voltage-probe` | `syntax-extension-candidate` | False | `checker_syntax_only_no_behavior_score` |
| `469-current-contribution-conductance` | `kcl-syntax-candidate` | False | `checker_syntax_only_no_behavior_score` |
| `470-branch-current-probe-contribution` | `kcl-syntax-candidate` | False | `checker_syntax_only_no_behavior_score` |
| `471-indirect-branch-null-balance` | `behavioral-continuous-time-candidate` | False | `checker_syntax_only_no_behavior_score` |
| `472-indirect-branch-ddt-balance` | `behavioral-continuous-time-candidate` | False | `checker_syntax_only_no_behavior_score` |
| `473-attribute-potential-abstol-probe` | `syntax-extension-candidate` | True | - |
| `474-generic-potential-access-function` | `syntax-extension-candidate` | True | - |
| `475-generic-potential-contribution` | `syntax-extension-candidate` | True | - |
| `476-oomr-string-voltage-probe` | `syntax-extension-candidate` | False | `checker_syntax_only_no_behavior_score` |
| `477-analog-node-alias-initial` | `syntax-extension-candidate` | False | `checker_syntax_only_no_behavior_score` |
| `478-inherited-port-attribute-supply` | `syntax-extension-candidate` | True | - |
| `479-inherited-mfactor-parameter` | `syntax-extension-candidate` | True | - |
| `480-mfactor-system-function-gain` | `syntax-extension-candidate` | False | `checker_syntax_only_no_behavior_score` |
| `481-analog-primitive-resistor-instance` | `kcl-syntax-candidate` | False | `checker_syntax_only_no_behavior_score` |
| `482-analog-primitive-isource-instance` | `kcl-syntax-candidate` | False | `checker_syntax_only_no_behavior_score` |
| `483-cds-violation-threshold-assert` | `cadence-simulator-function-candidate` | True | - |
| `484-rtoi-conversion-quantizer` | `syntax-extension-candidate` | True | - |
| `485-mc-trial-number-metric` | `cadence-simulator-function-candidate` | True | - |
| `486-rf-source-info-registration` | `cadence-simulator-function-candidate` | True | - |
| `487-table-model-2d-array-surface` | `syntax-extension-candidate` | False | `checker_syntax_only_no_behavior_score` |
| `488-table-model-string-param-source` | `syntax-extension-candidate` | False | `checker_syntax_only_no_behavior_score` |
| `489-event-nested-or-expression` | `syntax-extension-candidate` | True | - |
| `490-event-task-function-state-update` | `syntax-extension-candidate` | True | - |
| `491-kcl-capacitor-ddt-current` | `kcl-syntax-candidate` | False | `checker_syntax_only_no_behavior_score` |
| `492-kcl-inductor-idt-voltage` | `kcl-syntax-candidate` | False | `checker_syntax_only_no_behavior_score` |
| `493-continuous-laplace-nd-filter` | `behavioral-continuous-time-candidate` | False | `checker_syntax_only_no_behavior_score` |
| `494-continuous-zi-nd-filter` | `behavioral-continuous-time-candidate` | False | `checker_syntax_only_no_behavior_score` |
