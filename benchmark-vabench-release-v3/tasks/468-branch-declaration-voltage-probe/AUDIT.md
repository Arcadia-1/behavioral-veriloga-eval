# Audit: Branch Declaration Voltage Probe

- Task id: `v3_468_branch_declaration_voltage_probe`
- Category: `veriloga_branch_semantics`
- Gate 1 label: `l0_support_semantic`
- Certification scope: `language_extension_not_part_of_original_full_300_claim`
- Required semantic focus: explicit `branch (p, n) br;` declaration and `V(br)` voltage probing.

## Review Boundary

This task is retained as a Verilog-A branch semantic/support row. It is not counted as an independent AMS circuit function. The public prompt, starter, and checker should agree that `out` tracks the driven branch voltage `V(p,n)` through the named branch access.

## S4 Repair Notes

- Replaced the old prompt shape with the mandatory vaBench v3 instruction sections.
- Repaired the starter interface so it matches the public DUT ports.
- Updated the checker to derive expected samples from saved `p` and `n` waveforms instead of a fixed hidden sample table.
