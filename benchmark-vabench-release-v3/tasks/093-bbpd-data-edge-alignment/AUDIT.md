# Honest SOP Audit: Task 093 BBPD Data Edge Alignment

## Scope

Task boundary is one primary Verilog-A DUT artifact, `bbpd_data_edge_alignment_ref.va`, migrated from `vbr1_l1_bang_bang_phase_detector:tb`, plus the original EVAS/Spectre-compatible `.scs` transient scenario. Companion Verilog-A files listed in the top-level `TASKS.json` index are supplied by the harness when needed by the original system testbench.

## Four Standards

- Useful scenario: accepted. The module is a reusable behavioral Verilog-A block or flow component with a concrete transient use case.
- Reasonable task: accepted for this migration slice. The public prompt names the target artifact, interface, and behavior context.
- Complete tests: accepted for current v3 smoke. Hidden gold passes and `neg_001_zero` is non-full-credit; further hand-authored negatives can still strengthen release evidence.
- Fair evaluation: accepted for current v3 smoke. The checker is bound through the v3 alias and the hidden behavior is covered by the public prompt context.

## Checker And Evidence

- Source checker id: `vbr1_l1_bang_bang_phase_detector_tb`
- EVAS private-split gold and five concrete behavioral negatives: PASS/rejected in
  the current PLL/clock hygiene rerun.
- EVAS AHDL-like lint preflight on private decks: PASS with zero diagnostics.
- Spectre private-split gold was not rerun in this prompt-hygiene pass.

## Remaining Risk

Counting status remains an upstream benchmark-policy decision, but the public
prompt now states the BBPD data-edge timing contract directly instead of
listing private metric names or hidden-evaluator context.
