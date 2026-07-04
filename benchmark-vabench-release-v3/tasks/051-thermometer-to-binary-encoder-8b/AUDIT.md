# Task 051 Audit

Task: `051-thermometer-to-binary-encoder-8b`

## 2026-07 Testbench Utility Review

- Gate 1: retained as the inverse thermometer-to-binary support utility. It is distinct from task 050 because it validates ordered thermometer recognition, invalid-code handling, and output-valid behavior.
- Gate 2: public prompt now states the vector thermometer input, contiguous-from-`th0` validity rule, binary count output, `valid` behavior, bit order, thresholds, output levels, and voltage-domain constraints.
- Validation: with the EVAS2 integer-division parity fix from Arcadia-1/EVAS#80, the 24-row testbench-utility EVAS batch passed 24/24 gold cases and rejected 120/120 concrete negatives. Targeted Spectre gold coverage for this row passed. AHDL-like preflight reported no diagnostics for this row.
- EVAS note: this row exposed an evaluator bug where integer-typed division in bit-decode expressions was lowered as floating division. The benchmark prompt/gold were not weakened; the evaluator fix is covered in the EVAS PR.

Certification status: `cadence_modeling_ready` for support-formal scope, with EVAS#80 as the evaluator dependency for old EVAS2 revisions.
