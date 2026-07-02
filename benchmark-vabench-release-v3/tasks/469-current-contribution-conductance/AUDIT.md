# Audit: Current Contribution Conductance

- Task id: `v3_469_current_contribution_conductance`
- Category: `veriloga_kcl_contribution_semantics`
- Required syntax focus: `Use I(p,n) current contribution for a conductance-style model.`
- Certification scope: `language_extension_not_part_of_original_full_300_claim`
- Tier: `kcl-syntax-candidate`
- EVAS status: `behavior-certified for observable branch-current contribution`

## Behavior Certification

- Score claim: `extension_behavior_certified_outside_original_300`.
- Checker: `current_contribution_conductance_contract`.
- Observable: support artifact `branch_current_monitor.va` records `imon = I(p,n)` after DUT evaluation.
- Required behavior: `imon` tracks `1e-3 * V(p,n)` across visible and hidden p/n bias segments.
- Hidden coverage: p and n are driven independently, including a negative branch voltage, to catch absolute-node, positive-only, wrong-sign, offset, and wrong-scale implementations.
- Negative evidence: 5/5 variants are rejected by `FAIL_SIM_CORRECTNESS`.
- Promotion evidence: `benchmark-vabench-release-v3/reports/verify_301_494_layered.json` reports gold PASS and all five negatives rejected for this task.

## Boundary

This task certifies ordinary `I(p,n) <+ expr` contribution observability through a later `I(p,n)` probe. It does not claim full unknown-node MNA/KCL solving.
