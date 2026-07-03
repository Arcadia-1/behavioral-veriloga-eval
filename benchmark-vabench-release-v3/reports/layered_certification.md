# vaBench v3 Layered Certification

Date: 2026-07-03

## Headline

- Numbered default Spectre-compatible rows: **451**
- Original 001-300 rows retained in default denominator: **293**
- Numbered extension/replacement rows retained: **158**
- Unnumbered replacement candidates retained: **5**
- Spectre-rejected rows archived outside default denominator: **54**
- Full retained-row Spectre certification: **pending / case-by-case**

## Semantic Layers

| Layer | Tasks | Certification levels |
| --- | ---: | --- |
| `behavioral_continuous_time_extension` | 18 | spectre_compatible_extension_candidate: 18 |
| `behavioral_event_core` | 268 | behavior_certified_default_spectre_compatible: 268 |
| `behavioral_event_support` | 25 | behavior_certified_default_spectre_compatible: 25 |
| `behavioral_language_extension` | 117 | spectre_compatible_extension_candidate: 117 |
| `cadence_simulator_function_extension` | 3 | spectre_compatible_extension_candidate: 3 |
| `conservative_kcl_syntax_extension` | 6 | spectre_compatible_extension_candidate: 6 |
| `data_converter_replacement_candidate` | 7 | spectre_compatible_extension_candidate: 7 |
| `noise_analysis_extension` | 12 | spectre_compatible_extension_candidate: 12 |

## Claim Boundary

- The default tasks/ tree contains 451 numbered rows intended for the standalone-Spectre-compatible denominator plus five unnumbered candidates.
- Fifty-four rows that standalone Spectre rejects as written were moved to spectre-unsupported-tasks/ and removed from TASKS.json and CHECKS.yaml.
- The original 001-300 behavior-certified surface has 293 rows retained in the default denominator; rows 052-057 and 075 are archived because Spectre rejects their vector/indexing style.
- Retained extension rows are candidates until their EVAS, checker, and Spectre evidence are stated layer by layer.
- Continuous-time and KCL/current rows remain separate tiers from event-style behavioral rows.

## Completion Audit

- Status: `boundary_updated_not_full_spectre_certified`
- Complete: `false`
- Reason: The default denominator has been cleaned of rows known to be categorically rejected by standalone Spectre. Remaining retained rows still need case-by-case Spectre pass/fail audit and benchmark rewrites where needed.

| Requirement | Status | Evidence |
| --- | --- | --- |
| Remove rows that standalone Spectre rejects categorically from the default denominator. | `satisfied` | 54 rows archived under spectre-unsupported-tasks/ and removed from TASKS.json/CHECKS.yaml. |
| Keep archived rows available for future AMS/digital or version-gated suites. | `satisfied` | Task assets preserved under benchmark-vabench-release-v3/spectre-unsupported-tasks/. |
| Full retained-row Spectre behavior certification. | `pending` | Targeted Spectre reruns are recorded separately; retained failure rows require benchmark cleanup or focused EVAS/Spectre issues. |

## Archived Rows

See `spectre_unsupported_removed_20260703.md` for the 54 archived rows and reasons.
