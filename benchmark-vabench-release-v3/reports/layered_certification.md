# vaBench v3 Layered Certification

Date: 2026-07-02

## Headline

- Total tasks: **494**
- Original behavior-certified full-300 surface: **300**
- Extension candidates: **194**
- Behavior-certified extension rows: **173**
- Compile-supported candidate rows: **21**
- Unsupported candidate rows: **0**

## Semantic Layers

| Layer | Tasks | Certification levels |
| --- | ---: | --- |
| `ams_mixed_signal_extension` | 29 | behavior_certified_extension: 28, compile_supported_candidate: 1 |
| `behavioral_continuous_time_extension` | 14 | compile_supported_continuous_time_candidate: 14 |
| `behavioral_event_core` | 268 | behavior_certified: 268 |
| `behavioral_event_support` | 32 | behavior_certified_support: 32 |
| `behavioral_language_extension` | 130 | behavior_certified_extension: 130 |
| `cadence_simulator_function_extension` | 3 | behavior_certified_extension: 3 |
| `conservative_kcl_syntax_extension` | 6 | compile_supported_kcl_candidate: 6 |
| `noise_analysis_extension` | 12 | behavior_certified_extension: 12 |

## Blocking Issues

| EVAS issue | Blocked tasks | Semantic layers | Promotion acceptance |
| --- | ---: | --- | --- |
| https://github.com/Arcadia-1/EVAS/issues/44 | 18 | behavioral_continuous_time_extension: 14, conservative_kcl_syntax_extension: 4 | After EVAS support lands, promote the listed 18 task(s) by adding sim_correct behavior contracts/checkers if missing, then require 18/18 gold PASS, 90/90 negative variants rejected, and zero expectation_fail in the verification report. |
| https://github.com/Arcadia-1/EVAS/issues/48 | 1 | ams_mixed_signal_extension: 1 | After EVAS support lands, promote the listed 1 task(s) by adding sim_correct behavior contracts/checkers if missing, then require 1/1 gold PASS, 5/5 negative variants rejected, and zero expectation_fail in the verification report. |
| https://github.com/Arcadia-1/EVAS/issues/54 | 1 | conservative_kcl_syntax_extension: 1 | After EVAS support lands, promote the listed 1 task(s) by adding sim_correct behavior contracts/checkers if missing, then require 1/1 gold PASS, 5/5 negative variants rejected, and zero expectation_fail in the verification report. |
| https://github.com/Arcadia-1/EVAS/issues/55 | 1 | conservative_kcl_syntax_extension: 1 | After EVAS support lands, promote the listed 1 task(s) by adding sim_correct behavior contracts/checkers if missing, then require 1/1 gold PASS, 5/5 negative variants rejected, and zero expectation_fail in the verification report. |

## Completion Audit

- Status: `partial_external_blocked`
- Complete: `false`
- Reason: The full 301-494 objective is not complete because 21 extension tasks still lack behavior checker evidence and are excluded until EVAS support issues are resolved.

| Requirement | Status | Evidence | Gap |
| --- | --- | --- | --- |
| Scope covers all v3 extension tasks 301-494. | `satisfied` | layered_certification summary reports extension_candidate_count=194. |  |
| Each extension task has a clear prompt and required behavior section. | `satisfied` | extension_sop_audit has no missing_required_behavior_section issue. |  |
| Each extension task has executable visible and hidden test evidence. | `satisfied` | extension_sop_audit complete_tests_count=194. |  |
| Each extension task has five useful negative variants. | `satisfied` | extension_sop_audit reports no negative_count_lt5 issues. |  |
| Each extension task has repository behavior checker evidence and can be scored fairly. | `partial` | 173 extension tasks are behavior-certified; 21 remain excluded_until_behavior_promotion. | The remaining staged rows are blocked by EVAS support issues or missing behavior-checker evidence; staged_promotion_gold_probe records the current per-task blocker. |
| Behavior-certified extension tasks pass gold verification and reject all negative variants. | `satisfied` | verify_301_494_layered: gold_pass=173, gold_fail=0, negative_rejected=865, negative_accepted=0, expectation_fail=0. |  |
| Every staged task has a concrete EVAS issue and promotion checklist. | `satisfied` | 4 blocking issues cover 21 staged tasks; staged_promotion_gold_probe records 21/21 staged gold cases still failing the current promotion gate. |  |

## Claim Boundary

- Only tasks 001-300 are part of the original behavior-certified full-300 claim.
- Tasks 301-494 are extension candidates; they are excluded from score until promoted with behavior checkers and negative-case scoring.
- Compile-supported continuous-time rows do not certify continuous-time numeric accuracy.
- Compile-supported KCL rows do not certify MNA/KCL solving behavior.
- AMS, noise/analysis, Cadence-helper, and table-model extension rows require layer-specific behavior evidence before paper-facing promotion.

## Evidence Sources

| Evidence | Path / note |
| --- | --- |
| `task_manifest` | `benchmark-vabench-release-v3/TASKS.json` |
| `checker_manifest` | `benchmark-vabench-release-v3/CHECKS.yaml` |
| `extension_sop_audit` | `benchmark-vabench-release-v3/reports/extension_sop_audit.json` |
| `behavior_certified_extension_task_evidence` | `benchmark-vabench-release-v3/reports/behavior_certified_extension_task_evidence.json` |
| `language_extension_notes` | `benchmark-vabench-release-v3/LANGUAGE_EXTENSION.md` |
| `core_behavior_evidence` | `benchmark-vabench-release-v1/reports/benchmark_overview.json` |
| `staged_gold_probe` | `benchmark-vabench-release-v3/reports/staged_promotion_gold_probe.json` |
| `staged_gold_probe_summary` | `benchmark-vabench-release-v3/reports/staged_promotion_gold_probe.md` |
| `staged_blocker_matrix` | `benchmark-vabench-release-v3/reports/staged_blocker_matrix.json` |
| `staged_blocker_matrix_summary` | `benchmark-vabench-release-v3/reports/staged_blocker_matrix.md` |
| `latest_compile_probe` | `local evas-rust compile probe for tasks 460-494 solution plus five negative variants per task: 210 files, 0 failures` |
