# Audit: Branch Current Probe Contribution

- Task id: `v3_470_branch_current_probe_contribution`
- Category: `veriloga_kcl_contribution_semantics`
- Required syntax focus: `Use a named branch with current contribution and current probing.`
- EVAS status: `behavior-certified for named branch current contribution/probe`
- Score claim: `extension_behavior_certified_outside_original_300`.

## Behavior Certification

- Checker: `branch_current_probe_contribution_contract`.
- Required behavior: named branch current contributions are accumulated and later `I(br)` probes drive `out`.
- Visible/hidden coverage: hidden PWL bias points catch missing branch contribution, wrong thresholding, offset, and scale errors.
- Negative evidence: 5/5 variants are rejected by `FAIL_SIM_CORRECTNESS`.
- Evidence: `benchmark-vabench-release-v3/reports/verify_301_494_layered.json`.

## Boundary

This task certifies named-branch current observability in the behavioral checker. It does not claim full unknown-node MNA/KCL solving.
