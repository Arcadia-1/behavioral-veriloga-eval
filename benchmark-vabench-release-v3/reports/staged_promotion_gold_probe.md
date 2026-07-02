# v3 Staged Promotion Gold Probe

Date: 2026-07-02

This report records the current local EVAS gold-only promotion probe for the 38 staged v3 extension tasks. It is intentionally not a behavior-certification report: every row below remains excluded from score until its gold case passes and its five negative variants are rejected by a repository checker.

## Summary

- Scope: `301-494` staged tasks only
- Gold cases: **0/38 PASS**
- Expectation failures: **38**
- Skipped staged tasks: **0**
- Wall time: **7.622s**

## Per-Task Evidence

| Task | Layer | Status | Blocking issue | Current observed blocker |
| --- | --- | --- | --- | --- |
| `353-always-resettable-toggle` | `ams_mixed_signal_extension` | `FAIL_SIM_CORRECTNESS` | [#39](https://github.com/Arcadia-1/EVAS/issues/39) | no behavior checker implemented yet |
| `410-macro-ifdef-gain-select` | `behavioral_language_extension` | `FAIL_SIM_CORRECTNESS` | [#42](https://github.com/Arcadia-1/EVAS/issues/42) | no behavior checker implemented yet |
| `415-logic-vector-assign-slice` | `ams_mixed_signal_extension` | `FAIL_SIM_CORRECTNESS` | [#43](https://github.com/Arcadia-1/EVAS/issues/43) | no behavior checker implemented yet |
| `416-logic-vector-reduction-flag` | `ams_mixed_signal_extension` | `FAIL_SIM_CORRECTNESS` | [#43](https://github.com/Arcadia-1/EVAS/issues/43) | no behavior checker implemented yet |
| `417-always-async-reset-counter` | `ams_mixed_signal_extension` | `FAIL_SIM_CORRECTNESS` | [#39](https://github.com/Arcadia-1/EVAS/issues/39) | no behavior checker implemented yet |
| `418-always-enable-saturating-counter` | `ams_mixed_signal_extension` | `FAIL_SIM_CORRECTNESS` | [#43](https://github.com/Arcadia-1/EVAS/issues/43) | no behavior checker implemented yet |
| `431-hierarchy-support-artifact-staging` | `behavioral_language_extension` | `FAIL_TB_COMPILE` | [#41](https://github.com/Arcadia-1/EVAS/issues/41) | CompilationError: Unknown child module: staged_gain_child in hierarchy_support_artifact_staging.u_gain |
| `432-hierarchy-nested-parameter-chain` | `behavioral_language_extension` | `FAIL_TB_COMPILE` | [#41](https://github.com/Arcadia-1/EVAS/issues/41) | CompilationError: Unknown child module: staged_gain_child in hierarchy_nested_parameter_chain.u_gain0 |
| `435-ddt-voltage-derivative-source` | `behavioral_continuous_time_extension` | `FAIL_SIM_CORRECTNESS` | [#44](https://github.com/Arcadia-1/EVAS/issues/44) | no behavior checker implemented yet |
| `436-idt-voltage-integrator-source` | `behavioral_continuous_time_extension` | `FAIL_SIM_CORRECTNESS` | [#44](https://github.com/Arcadia-1/EVAS/issues/44) | no behavior checker implemented yet |
| `437-laplace-nd-lowpass-filter` | `behavioral_continuous_time_extension` | `FAIL_SIM_CORRECTNESS` | [#44](https://github.com/Arcadia-1/EVAS/issues/44) | no behavior checker implemented yet |
| `438-laplace-np-pole-filter` | `behavioral_continuous_time_extension` | `FAIL_SIM_CORRECTNESS` | [#44](https://github.com/Arcadia-1/EVAS/issues/44) | no behavior checker implemented yet |
| `439-laplace-zd-zero-den-filter` | `behavioral_continuous_time_extension` | `FAIL_SIM_CORRECTNESS` | [#44](https://github.com/Arcadia-1/EVAS/issues/44) | no behavior checker implemented yet |
| `440-laplace-zp-zero-pole-filter` | `behavioral_continuous_time_extension` | `FAIL_SIM_CORRECTNESS` | [#44](https://github.com/Arcadia-1/EVAS/issues/44) | no behavior checker implemented yet |
| `441-zi-nd-discrete-filter` | `behavioral_continuous_time_extension` | `FAIL_SIM_CORRECTNESS` | [#44](https://github.com/Arcadia-1/EVAS/issues/44) | no behavior checker implemented yet |
| `442-zi-np-discrete-filter` | `behavioral_continuous_time_extension` | `FAIL_SIM_CORRECTNESS` | [#44](https://github.com/Arcadia-1/EVAS/issues/44) | no behavior checker implemented yet |
| `443-zi-zd-discrete-filter` | `behavioral_continuous_time_extension` | `FAIL_SIM_CORRECTNESS` | [#44](https://github.com/Arcadia-1/EVAS/issues/44) | no behavior checker implemented yet |
| `444-zi-zp-discrete-filter` | `behavioral_continuous_time_extension` | `FAIL_SIM_CORRECTNESS` | [#44](https://github.com/Arcadia-1/EVAS/issues/44) | no behavior checker implemented yet |
| `449-generate-genvar-replicated-stage` | `behavioral_language_extension` | `FAIL_SIM_CORRECTNESS` | [#45](https://github.com/Arcadia-1/EVAS/issues/45) | no behavior checker implemented yet |
| `453-specify-specparam-delay` | `ams_mixed_signal_extension` | `FAIL_SIM_CORRECTNESS` | [#48](https://github.com/Arcadia-1/EVAS/issues/48) | no behavior checker implemented yet |
| `455-packed-logic-bus-slice` | `ams_mixed_signal_extension` | `FAIL_SIM_CORRECTNESS` | [#43](https://github.com/Arcadia-1/EVAS/issues/43) | no behavior checker implemented yet |
| `464-param-given-gain-select` | `behavioral_language_extension` | `FAIL_SIM_CORRECTNESS` | [#49](https://github.com/Arcadia-1/EVAS/issues/49) | no behavior checker implemented yet |
| `468-branch-declaration-voltage-probe` | `behavioral_language_extension` | `FAIL_SIM_CORRECTNESS` | [#50](https://github.com/Arcadia-1/EVAS/issues/50) | no behavior checker implemented yet |
| `469-current-contribution-conductance` | `conservative_kcl_syntax_extension` | `FAIL_SIM_CORRECTNESS` | [#44](https://github.com/Arcadia-1/EVAS/issues/44) | no behavior checker implemented yet |
| `470-branch-current-probe-contribution` | `conservative_kcl_syntax_extension` | `FAIL_SIM_CORRECTNESS` | [#44](https://github.com/Arcadia-1/EVAS/issues/44) | no behavior checker implemented yet |
| `471-indirect-branch-null-balance` | `behavioral_continuous_time_extension` | `FAIL_SIM_CORRECTNESS` | [#44](https://github.com/Arcadia-1/EVAS/issues/44) | no behavior checker implemented yet |
| `472-indirect-branch-ddt-balance` | `behavioral_continuous_time_extension` | `FAIL_SIM_CORRECTNESS` | [#44](https://github.com/Arcadia-1/EVAS/issues/44) | no behavior checker implemented yet |
| `476-oomr-string-voltage-probe` | `behavioral_language_extension` | `FAIL_SIM_CORRECTNESS` | [#51](https://github.com/Arcadia-1/EVAS/issues/51) | out@50ns=0.0000 expected=0.2000 tol=0.0350 |
| `477-analog-node-alias-initial` | `behavioral_language_extension` | `FAIL_SIM_CORRECTNESS` | [#52](https://github.com/Arcadia-1/EVAS/issues/52) | out@50ns=0.0000 expected=0.2000 tol=0.0350 |
| `480-mfactor-system-function-gain` | `behavioral_language_extension` | `FAIL_DUT_COMPILE` | [#53](https://github.com/Arcadia-1/EVAS/issues/53) | ERROR: Failed to compile Verilog-A file mfactor_system_function_gain.va: Spectre-incompatible/unsupported Verilog-A function call: $mfactor() |
| `481-analog-primitive-resistor-instance` | `conservative_kcl_syntax_extension` | `FAIL_TB_COMPILE` | [#54](https://github.com/Arcadia-1/EVAS/issues/54) | CompilationError: Unknown child module: resistor in analog_primitive_resistor_instance.rload |
| `482-analog-primitive-isource-instance` | `conservative_kcl_syntax_extension` | `FAIL_TB_COMPILE` | [#55](https://github.com/Arcadia-1/EVAS/issues/55) | CompilationError: Unknown child module: isource in analog_primitive_isource_instance.ib |
| `487-table-model-2d-array-surface` | `behavioral_language_extension` | `FAIL_SIM_CORRECTNESS` | [#56](https://github.com/Arcadia-1/EVAS/issues/56) | out@50ns=0.0000 expected=1.0000 tol=0.0500 |
| `488-table-model-string-param-source` | `behavioral_language_extension` | `FAIL_SIM_CORRECTNESS` | [#40](https://github.com/Arcadia-1/EVAS/issues/40) | out@10ns=0.0000 expected=0.1000 tol=0.0400 |
| `491-kcl-capacitor-ddt-current` | `conservative_kcl_syntax_extension` | `FAIL_SIM_CORRECTNESS` | [#44](https://github.com/Arcadia-1/EVAS/issues/44) | no behavior checker implemented yet |
| `492-kcl-inductor-idt-voltage` | `conservative_kcl_syntax_extension` | `FAIL_SIM_CORRECTNESS` | [#44](https://github.com/Arcadia-1/EVAS/issues/44) | returncode=1; evas_engine=python; tran.csv missing |
| `493-continuous-laplace-nd-filter` | `behavioral_continuous_time_extension` | `FAIL_SIM_CORRECTNESS` | [#44](https://github.com/Arcadia-1/EVAS/issues/44) | no behavior checker implemented yet |
| `494-continuous-zi-nd-filter` | `behavioral_continuous_time_extension` | `FAIL_SIM_CORRECTNESS` | [#44](https://github.com/Arcadia-1/EVAS/issues/44) | no behavior checker implemented yet |

## Promotion Gate

A staged task can move to behavior-certified only after all of the following are true:

- Gold solution passes with the intended visible/hidden behavior.
- Five negative variants are rejected by a behavior checker, not merely by missing support.
- CHECKS.yaml includes `sim_correct` positive/negative paths and required trace columns.
- AUDIT.md documents the promotion evidence and EVAS issue boundary is removed or narrowed.