# Audit: Hierarchy Support Artifact Staging

- Task id: `v3_431_hierarchy_support_artifact_staging`
- Category: `veriloga_hierarchy_semantics`
- Required syntax focus: `Use a parent module plus staged support child artifact in the same source.`
- EVAS status: `behavior-certified`
- Score claim: `extension_behavior_certified_outside_original_300`.

## Behavior Certification

- Checker: `hierarchy_support_artifact_staging_contract`.
- Required behavior: parent and support child artifacts are staged together and produce the expected chained gain behavior.
- Visible/hidden coverage: hidden stimulus changes input segments to catch missing child staging, hard-coded outputs, and wrong child gain.
- Negative evidence: 5/5 variants are rejected by `FAIL_SIM_CORRECTNESS`.
- Evidence: `benchmark-vabench-release-v3/reports/verify_301_494_layered.json`.

## Boundary

This task certifies flat support-artifact staging and behavioral child-module evaluation for the benchmark harness. It does not expand the original full-300 denominator.
