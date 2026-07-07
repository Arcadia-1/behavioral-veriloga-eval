# Audit Summary

- Task id: `v3_056_correlated_double_sampler`
- Gate 1: `independent_l1_ready`
- Gate 2: `cadence_modeling_ready`
- Issue #109 action: replaces the previous deterministic mismatch DAC6 candidate, which was too close to `027-dac-mismatch-unit-weighting-model` under strict duplicate/counting review.
- Function boundary: two-phase correlated double sampler for a data-converter/front-end path. The DUT captures reset and signal samples on separate voltage-coded clocks, outputs a held signal-minus-reset correction, and exposes valid state.
- Independence evidence: no active v3 row matches a correlated reset/signal double-sampling correction. Existing sample/hold rows (`026`, `044`, `080`, `081`, `109`, `114`) capture or hold analog levels but do not form a paired reset-level subtraction. Existing ADC/DAC rows quantize or reconstruct codes and do not evaluate this front-end correction boundary.
- Cadence/source basis: Cadence Verilog-A course notes in `_local_learning/vaevas-cadence-notes` emphasize event-detected sampling, stateful sample/hold behavior, held historical values, transition-smoothed outputs, and explicit prompt contracts for ADC/DAC bus/interface rows. This task packages that documented Spectre modeling style as a circuit-meaningful data-converter front-end primitive rather than as an operator-only row.
- Prompt hygiene: uses the mandatory vaBench v3 heading shape with explicit interface, parameter contract, required behavior, modeling constraints, and output contract.
- Hidden coverage: hidden deck changes reset/signal phase timing, input sequence, positive and negative deltas, and low/high clipping relative to visible. It is not byte-identical or comment-only.
- Negative coverage: five concrete negatives cover stuck output, continuous tracking, reversed subtraction sign, missing reset sample, and valid not clearing during reset reacquisition.
- Certification status: fresh issue #109 validation passes EVAS visible and hidden gold, rejects all five EVAS visible and hidden negative variants, passes Spectre visible and hidden gold, rejects all five Spectre visible and hidden negative variants, and passes the full seven-row hidden Spectre batch with `7/7` gold PASS and `35/35` hidden negatives rejected.
