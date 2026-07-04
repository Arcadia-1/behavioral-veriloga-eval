# Audit: Above Resettable Peak Marker

## Gate 1 Classification

- Classification: L0/support boundary.
- Circuit role: `above()`-armed sampled peak marker.
- Counting note: this row primarily exercises Cadence/Verilog-A operator or syntax semantics. As written, it should not be counted as a new independent core circuit-function benchmark without a separate rescue decision.

## Gate 2 Modeling Notes

- The public prompt is normalized to the v3 instruction headings.
- The DUT contract is voltage-domain behavioral Verilog-A and avoids transistor-level devices and current-domain branch contributions.
- Public parameter values, event thresholds, output scaling, reset behavior, and smoothing requirements are stated in the prompt where they are part of the observable contract.
- Testbench values are not presented as implementation constants to copy into the DUT.

## Validation Notes

- EVAS2 reference run: PASS for this row in the 326-340 batch after the EVAS idtmod/random/last_crossing semantic fixes.
- EVAS2 negative run: the 326-340 batch produced 90/90 expectation matches; after strengthening `neg_004_logic_threshold_shifted`, the 327/335 local retest produced 12/12 expectation matches.
- Spectre reference run: PASS for this row in the targeted 326-340 private validation batch.
- Spectre negative run: the first full negative pass exposed `neg_004_logic_threshold_shifted` as too weak under Spectre; after shifting the `above()` threshold and restoring peak accumulation, the row-specific retest rejected it behaviorally.
- AHDL-like lint: PASS with zero diagnostics.
