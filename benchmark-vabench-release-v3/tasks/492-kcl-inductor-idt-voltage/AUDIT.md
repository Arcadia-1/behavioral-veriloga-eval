# Audit: Kcl Inductor Idt Voltage

- Task id: `v3_492_kcl_inductor_idt_voltage`
- Category: `veriloga_kcl_contribution_semantics`
- Gate 1 label: `l0_support_semantic`
- Certification scope: `language_extension_not_part_of_original_full_300_claim`
- Required semantic focus: `idt(I(p,n), 0.0)` inside a conservative voltage contribution.

## Review Boundary

This task is retained as a conservative-current/continuous-operator semantic/support row. It is useful for evaluator and simulator compatibility, but should not be counted as an ordinary independent voltage-domain AMS L1 circuit function.

## S4 Repair Notes

- Replaced the old prompt shape with the mandatory vaBench v3 instruction sections.
- Replaced the solution-equivalent starter with an incomplete but interface-correct starting point.
- Updated the checker so visible validation does not require hidden-only late samples.
