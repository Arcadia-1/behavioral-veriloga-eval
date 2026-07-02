# vaBench v3 Layered Certification

Date: 2026-07-02

## Headline

- Total tasks: **501**
- Original behavior-certified full-300 surface: **300**
- Extension candidates: **201**
- Behavior-certified extension rows: **201**
- Compile-supported candidate rows: **0**
- Unsupported candidate rows: **0**

## Semantic Layers

| Layer | Tasks | Certification levels |
| --- | ---: | --- |
| `ams_mixed_signal_extension` | 29 | behavior_certified_extension: 29 |
| `behavioral_continuous_time_extension` | 14 | behavior_certified_extension: 14 |
| `behavioral_event_core` | 268 | behavior_certified: 268 |
| `behavioral_event_support` | 32 | behavior_certified_support: 32 |
| `behavioral_language_extension` | 130 | behavior_certified_extension: 130 |
| `cadence_simulator_function_extension` | 3 | behavior_certified_extension: 3 |
| `conservative_kcl_syntax_extension` | 6 | behavior_certified_extension: 6 |
| `data_converter_replacement_candidate` | 7 | behavior_certified_extension: 7 |
| `noise_analysis_extension` | 12 | behavior_certified_extension: 12 |

## Blocking Issues

| EVAS issue | Blocked tasks | Semantic layers | Promotion acceptance |
| --- | ---: | --- | --- |

## Completion Audit

- Status: `complete`
- Complete: `true`
- Reason: All 201 extension tasks have behavior checker evidence, gold verification, and five rejected negative variants.

| Requirement | Status | Evidence | Gap |
| --- | --- | --- | --- |
| Scope covers all v3 extension tasks 301-501. | `satisfied` | layered_certification summary reports extension_candidate_count=201. |  |
| Each extension task has a clear prompt and required behavior section. | `satisfied` | extension_sop_audit has no missing_required_behavior_section issue. |  |
| Each extension task has executable visible and hidden test evidence. | `satisfied` | extension_sop_audit complete_tests_count=201. |  |
| Each extension task has five useful negative variants. | `satisfied` | extension_sop_audit reports no negative_count_lt5 issues. |  |
| Each extension task has repository behavior checker evidence and can be scored fairly. | `satisfied` | 201 extension tasks are behavior-certified; 0 remain excluded_until_behavior_promotion. |  |
| Behavior-certified extension tasks pass gold verification and reject all negative variants. | `satisfied` | verify_301_501_layered: gold_pass=201, gold_fail=0, negative_rejected=1005, negative_accepted=0, expectation_fail=0. |  |
| Every staged task has a concrete EVAS issue and promotion checklist. | `satisfied` | No staged tasks remain; no EVAS promotion blockers are required. |  |

## Claim Boundary

- Only tasks 001-300 are part of the original behavior-certified full-300 claim.
- Tasks 301-501 are behavior-certified extension rows outside the original full-300 denominator.
- Continuous-time rows certify the repository's finite-difference/stateful behavioral response, not a general analog solver accuracy claim.
- KCL/current rows certify observable branch-current contribution behavior, not unknown-node MNA/KCL solving.
- AMS, noise/analysis, Cadence-helper, Cadence-derived data-converter, and table-model extension rows are certified only for their layer-specific transient/checker contracts.

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
| `latest_compile_probe` | `local EVAS compile/verification probes cover the current staging rows and their five negative variants per task.` |
