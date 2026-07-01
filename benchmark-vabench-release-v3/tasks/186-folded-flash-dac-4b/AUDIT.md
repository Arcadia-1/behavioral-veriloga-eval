# Folded Flash DAC 4b Audit

- Gate 1: kept as the folded 4-bit DAC row. The near-duplicate `293-flash-folded-dac4` should not be counted separately unless it is rewritten into a distinct folded-DAC behavior.
- Public contract: decode lower-bit subcode weights 4, 2, and 1, use the MSB as the folded branch selector, and scale the folded code by `vref/16`.
- Cadence reference correspondence: the local Cadence DAC reference models code-to-voltage conversion and clock/transition-aware output driving; this benchmark uses the same code-to-voltage concept with a folded transfer.
- Duplicate review: `186` and `293` implement the same folded branch behavior under different names. `186` is retained because its public prompt is cleaner and the solution already exposes transition timing parameters.
- Evaluation note: hidden coverage should use a code sequence distinct from visible smoke, and checker expectations should be derived from saved input code bits.
