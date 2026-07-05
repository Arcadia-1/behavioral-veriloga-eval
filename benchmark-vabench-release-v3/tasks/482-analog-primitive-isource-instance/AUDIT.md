# Audit: Analog Primitive Isource Instance

- Task id: `v3_482_analog_primitive_isource_instance`
- Category: `veriloga_analog_primitive_semantics`
- Gate 1 label: `l0_support_semantic`
- Certification scope: `language_extension_not_part_of_original_full_300_claim`
- Required semantic focus: Spectre-style current-source primitive instance structure.

## Review Boundary

This task is retained as a structure-certified analog-primitive semantic/support row. It certifies the source artifact shape for a primitive instance and does not claim current-source circuit behavior or full MNA/KCL behavior.

## S4 Repair Notes

- Replaced the old prompt shape with the mandatory vaBench v3 instruction sections.
- Clarified TASKS metadata so it no longer claims KCL behavior certification.
- Replaced the solution-equivalent starter with an incomplete but interface-correct starting point.
