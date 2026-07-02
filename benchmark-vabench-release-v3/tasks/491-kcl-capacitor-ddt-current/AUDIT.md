# Audit: Kcl Capacitor Ddt Current

- Task id: `v3_491_kcl_capacitor_ddt_current`
- Category: `veriloga_kcl_contribution_semantics`
- Required syntax focus: `Use current contribution with ddt() for a capacitor-style conservative model.`
- Certification scope: `language_extension_not_part_of_original_full_300_claim`
- Tier: `kcl-syntax-candidate`
- EVAS status: `behavior-certified for observable ddt branch-current contribution`

## Behavior Certification

- Score claim: `extension_behavior_certified_outside_original_300`.
- Checker: `kcl_capacitor_ddt_current_contract`.
- Observable: support artifact `branch_current_monitor.va` records `imon = I(p,n)` after DUT evaluation.
- Required behavior: `imon` tracks `1p * ddt(V(p,n))` on rising and falling branch-voltage ramps.
- Hidden coverage: p and n both move, so `ddt(V(p))` can pass a grounded-reference smoke test but fails the dynamic-reference hidden checks.
- Negative evidence: 5/5 variants are rejected by `FAIL_SIM_CORRECTNESS`.
- Promotion evidence: `benchmark-vabench-release-v3/reports/verify_301_494_layered.json` reports gold PASS and all five negatives rejected for this task.

## Boundary

This task certifies finite-difference behavioral `ddt(V(p,n))` branch-current observability. It does not claim full unknown-node MNA/KCL capacitor loading.
