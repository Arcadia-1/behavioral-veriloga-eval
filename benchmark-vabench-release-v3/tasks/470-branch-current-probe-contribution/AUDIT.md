# Audit: Branch Current Probe Contribution

- Task id: `v3_470_branch_current_probe_contribution`
- Category: `veriloga_kcl_contribution_semantics`
- Gate 1 label: `l0_support_semantic`
- Certification scope: `language_extension_not_part_of_original_full_300_claim`
- Required semantic focus: named branch current contribution and later `I(br)` probing.

## Review Boundary

This task is retained as a conservative-current branch semantic/support row. It checks named branch current contribution/probe behavior, but does not by itself establish a scored standalone AMS circuit function.

## S4 Repair Notes

- Replaced the old prompt shape with the mandatory vaBench v3 instruction sections.
- Repaired the starter interface so it matches the public DUT ports.
- Updated the checker to derive expected monitor values from saved `p` and `n` waveforms and to cover the longer hidden stimulus when present.
