# Audit: Attribute Potential Abstol Probe

- Task id: `v3_473_attribute_potential_abstol_probe`
- Category: `veriloga_attribute_semantics`
- Gate 1 label: `l0_support_semantic`
- Certification scope: `language_extension_not_part_of_original_full_300_claim`
- Required semantic focus: `in.potential.abstol` attribute access and voltage-domain observation.

## Review Boundary

This task is retained as an electrical-attribute semantic/support row. It is not counted as an independent AMS circuit function.

## S4 Repair Notes

- Replaced the old prompt shape with the mandatory vaBench v3 instruction sections.
- Updated the checker to compute expected output from saved `inp` plus the public abstol-derived offset.
