# Issue #29 — v3 Duplicate and Filler Audit Report

Generated: issue29_duplicate_and_filler_audit
Tasks scanned: 300

## Overview

Forms: {'dut': 296, 'e2e': 2, 'tb': 1, 'bugfix': 1}
Difficulties: {'D2': 235, 'D3': 8, 'D1': 57}
Negative count: min=0, median=4, max=6
Tasks with ≤1 negative: 76

## Identical Solution Groups

- 099-dither-adder
- 101-fixed-gain-amplifier
- 111-clocked-sine-source

## Duplicate / Variant Pairs

### 007-first-order-lowpass × 286-first-order-lowpass-bugfix
- Classification: valid_variant_needs_counting_policy
- Recommendation: Same solution in different artifact forms. Keep as separate skills but adjust counting labels.

### 049-window-comparator-detector × 284-window-comparator-testbench
- Classification: valid_variant_needs_counting_policy
- Recommendation: Same solution in different artifact forms. Keep as separate skills but adjust counting labels.

### 081-aperture-delay-track-and-hold × 285-aperture-delay-sample-hold
- Classification: exact_duplicate_needs_merge
- Recommendation: Identical solution in same form. Differentiate instruction/checker/negatives or merge.

### 097-cppll-tracking-reacquire-timer × 107-reference-step-clock
- Classification: exact_duplicate_needs_merge
- Recommendation: Identical solution in same form. Differentiate instruction/checker/negatives or merge.

## Weak-Negative Tasks (≤1 negative)

- 011-pfd-up-dn-logic
- 012-clock-divider
- 013-resettable-integrator
- 014-sar-logic
- 015-segmented-dac
- 016-binary-weighted-voltage-dac
- 017-slew-rate-limiter
- 018-strongarm-style-latch-comparator
- 019-unit-element-thermometer-dac
- 020-thermometer-code-decoder
- 021-vco-phase-integrator
- 022-bandgap-reference-macro-model
- 023-calibration-deadband-controller
- 024-charge-pump-abstraction
- 025-clocked-adc-quantizer
- 026-clocked-sample-and-hold
- 027-dac-mismatch-unit-weighting-model
- 028-digital-phase-accumulator-with-modulo-wrap
- 029-dwa-dem-encoder
- 030-higher-order-filter
- 031-hysteresis-comparator
- 032-ldo-regulator-macro-model
- 033-limiting-amplifier-frontend
- 034-lna-gain-compression-macro
- 035-log-rssi-power-detector
- 036-loop-filter-abstraction
- 037-pa-compression-macro
- 038-power-on-reset-detector
- 039-precision-rectifier-envelope-detector
- 040-programmable-gain-amplifier
- 041-propagation-delay-comparator
- 042-ptat-ctat-reference-generator
- 043-rf-mixer-downconverter-macro
- 044-sample-and-hold-with-droop-leakage
- 045-soft-hysteretic-limiter
- 046-successive-approximation-calibration-search-fsm
- 047-threshold-comparator
- 048-uvlo-brownout-detector
- 049-window-comparator-detector
- 080-acquisition-limited-sample-and-hold
- 081-aperture-delay-track-and-hold
- 082-bias-voltage-generator-with-enable-trim
- 083-crossing-metric-writer
- 084-peak-detector
- 085-burst-clock-source
- 086-dither-noise-like-deterministic-source
- 087-lfsr-prbs-generator
- 088-ramp-step-source
- 089-sine-periodic-voltage-source
- 090-adpll-ratio-hop-timer
- 091-agc-receiver-leveling-loop
- 092-amplifier-filter-chain
- 093-bbpd-data-edge-alignment
- 094-comparator-offset-search
- 095-complete-calibration-loop
- 096-converter-static-linearity-measurement
- 097-cppll-tracking-reacquire-timer
- 098-edge-crossing-interval-timer
- 099-dither-adder
- 100-final-step-file-metric
- 101-fixed-gain-amplifier
- 102-gain-estimator
- 103-iq-downconversion-chain
- 104-ldo-load-step-recovery
- 105-pipeline-adc-chain-4b
- 106-programmable-stimulus-sequencer
- 107-reference-step-clock
- 108-reference-startup-enable-flow
- 109-sample-hold-droop-front-end
- 110-settling-time-measurement
- 111-clocked-sine-source
- 283-weighted-sar-adc-dac-loop
- 284-window-comparator-testbench
- 285-aperture-delay-sample-hold
- 286-first-order-lowpass-bugfix
- 287-gain-extraction-flow

## Release Wording Recommendation

Until duplicate/high-overlap groups are resolved, describe v3 as "300 candidate task directories" rather than "300 high-quality independent tasks".
