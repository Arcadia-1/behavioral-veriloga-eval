# vaBench v3 Layered Certification

Date: 2026-07-01

## Headline

- Total tasks: **494**
- Original behavior-certified full-300 surface: **300**
- Extension candidates: **194**
- Behavior-certified extension rows: **22**
- Compile-supported candidate rows: **172**
- Unsupported candidate rows: **0**

## Semantic Layers

| Layer | Tasks | Certification levels |
| --- | ---: | --- |
| `ams_mixed_signal_extension` | 26 | compile_supported_candidate: 26 |
| `behavioral_continuous_time_extension` | 4 | compile_supported_continuous_time_candidate: 4 |
| `behavioral_event_core` | 268 | behavior_certified: 268 |
| `behavioral_event_support` | 32 | behavior_certified_support: 32 |
| `behavioral_language_extension` | 143 | behavior_certified_extension: 22, compile_supported_candidate: 121 |
| `cadence_simulator_function_extension` | 3 | compile_supported_candidate: 3 |
| `conservative_kcl_syntax_extension` | 6 | compile_supported_kcl_candidate: 6 |
| `noise_analysis_extension` | 12 | compile_supported_candidate: 12 |

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
| `language_extension_notes` | `benchmark-vabench-release-v3/LANGUAGE_EXTENSION.md` |
| `core_behavior_evidence` | `benchmark-vabench-release-v1/reports/benchmark_overview.json` |
| `latest_compile_probe` | `local evas-rust compile probe for tasks 460-494 solution plus five negative variants per task: 210 files, 0 failures` |
