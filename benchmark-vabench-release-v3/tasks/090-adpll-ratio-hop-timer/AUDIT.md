# Honest SOP Audit: Task 090 ADPLL Ratio Hop Timer

## Scope

Task boundary is one primary Verilog-A DUT artifact, `adpll_ratio_hop_ref.va`, migrated from `vbr1_l2_adpll_lock_ratio_hop_timer_flow:tb`, plus the original EVAS/Spectre-compatible `.scs` transient scenario. Companion Verilog-A files listed in the top-level `TASKS.json` index are supplied by the harness when needed by the original system testbench.

## Four Standards

- Useful scenario: accepted. The module is a reusable behavioral Verilog-A block or flow component with a concrete transient use case.
- Reasonable task: accepted for this migration slice. The public prompt names the target artifact, interface, and behavior context.
- Complete tests: accepted for current v3 smoke. Hidden gold passes and `neg_001_zero` is non-full-credit; further hand-authored negatives can still strengthen release evidence.
- Fair evaluation: accepted for current v3 smoke. The checker is bound through the v3 alias and the hidden behavior is covered by the public prompt context.

## Checker And Evidence

- Source checker id: `vbr1_l2_adpll_lock_ratio_hop_timer_flow_tb`
- EVAS private-split gold and five concrete behavioral negatives: PASS/rejected in
  the current PLL/clock hygiene rerun.
- EVAS AHDL-like lint preflight on private decks: PASS with zero diagnostics
  after smoothing the control-code monitor output.
- Spectre 21.1 private-split gold audit: PASS in the current PLL/clock hygiene rerun.

## Remaining Risk

Counting status remains an upstream benchmark-policy decision, but the public
prompt no longer depends on private-evaluator context wording and the current gold has
EVAS negative, EVAS lint-preflight, and Spectre private-split gold evidence.
