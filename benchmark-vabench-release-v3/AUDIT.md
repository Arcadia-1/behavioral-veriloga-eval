# v3 Task Quality Audit

This file records durable public audit status for the v3 task set. It is not a
private Vela run log.

## Source-Series Audit

As of 2026-06-26, v3 contains 185 `source-*` tasks. The initial source-series
audit found that most imported source tasks had only one concrete negative
variant, usually `neg_001_zero`. That is not strong enough for the final
benchmark standard because it proves little beyond "not all outputs are zero."

The source-series repair is being done in batches. Each repaired batch should
meet these minimum conditions:

- public task contract and implementation boundary are clear;
- gold solution passes the EVAS checker through the normal task id path;
- each task has multiple concrete behavior negatives, not only all-zero;
- every new negative compiles and fails behavioral correctness rather than
  failing by syntax or missing files.

## Completed Pilot: 288-300

Tasks `288-source-absolute-value` through
`300-source-pfd-active-low-reset` were used as the first source-series repair
pilot.

Changes made:

- each task now has four negative variants: the original `neg_001_zero` plus
  three targeted behavior mutations;
- `runners/simulate_evas.py` registers checker aliases for the task ids
  `v3_288_source_*` through `v3_300_source_*`, so the normal `task.toml` id path
  reaches the checker without requiring a manual `--checker-task-id` override.

EVAS 0.4.5 local verification:

- 13/13 gold solutions PASS;
- 52/52 concrete negative variants fail behavioral correctness;
- no negative variant passed unexpectedly.

## Completed Batch: 112-127

Tasks `112-source-clocked-sar-comparator` through
`127-source-sar-weighted-sum` were repaired as the second source-series batch.

Changes made:

- each task now has four negative variants: the original `neg_001_zero` plus
  three targeted behavior mutations;
- task `123-source-start-gated-offset-search` gold was corrected so START is
  handled as an explicit enable transition instead of a continuous reset;
- source checker aliases now cover the normal `task.toml` ids for this batch.

EVAS 0.4.5 local verification:

- 16/16 gold solutions PASS;
- 64/64 concrete negative variants fail behavioral correctness;
- no negative variant passed unexpectedly.

## Completed Batch: 176-191

Tasks `176-source-dual-modulus-divider-16-17` through
`191-source-dac-8bit-ideal-scalar` were repaired as the sixth source-series
batch.

Changes made:

- each task now has four negative variants: the original `neg_001_zero` plus
  three targeted behavior mutations;
- the new negatives cover divider modulus and duty mistakes, serial and cyclic
  decoder normalization mistakes, flash-threshold mistakes, current/delayed
  output mistakes, sample-demux channel mistakes, DAC weight and polarity
  mistakes, folded-DAC mirror mistakes, residue/normalization mistakes, and
  scalar DAC bit-order mistakes;
- weak candidate negatives that were hidden-test equivalent or below tolerance
  were replaced with distinguishable behavioral failures.

EVAS 0.4.5 local verification:

- 16/16 gold solutions PASS;
- 64/64 concrete negative variants fail behavioral correctness;
- no negative variant passed unexpectedly.

## Completed Batch: 192-207

Tasks `192-source-flash-data-align-pipeline` through
`207-source-iterative-isar-dac` were repaired as the seventh source-series
batch.

Changes made:

- each task now has four negative variants: the original `neg_001_zero` plus
  three targeted behavior mutations;
- the new negatives cover pipeline latency and output bit-order mistakes,
  cyclic-decoder normalization mistakes, ADC/DAC weight and polarity mistakes,
  residue-control mistakes, clock-mux count mistakes, comparator reset and
  polarity mistakes, edge-align lane mistakes, serial accumulation mistakes,
  nonbinary SAR weight mistakes, and iterative DAC search-step mistakes;
- weak candidate negatives that were hidden-test equivalent or parameter
  equivalent were replaced with distinguishable behavioral failures.

EVAS 0.4.5 local verification:

- 16/16 gold solutions PASS;
- 64/64 concrete negative variants fail behavioral correctness;
- no negative variant passed unexpectedly.

## Completed Batch: 160-175

Tasks `160-source-voltage-controlled-gain-amplifier` through
`175-source-four-channel-edge-sampler` were repaired as the fifth source-series
batch.

Changes made:

- each task now has four negative variants: the original `neg_001_zero` plus
  three targeted behavior mutations;
- the new negatives cover controlled-gain mistakes, differential polarity and
  common-mode mistakes, adder/subtractor truth-table mistakes, latch hold and
  complement mistakes, ADC/DAC quantization mistakes, sample-delay mistakes,
  mux decode mistakes, clock-divider duty/phase mistakes, weighted decoder
  mistakes, bit-encoder mistakes, and multi-channel sampler mistakes;
- weak edge-trigger negatives that were equivalent under the current hidden
  stimulus were replaced with distinguishable behavioral failures.

EVAS 0.4.5 local verification:

- 16/16 gold solutions PASS;
- 64/64 concrete negative variants fail behavioral correctness;
- no negative variant passed unexpectedly.

## Completed Batch: 144-159

Tasks `144-source-differential-deadband` through
`159-source-variable-gain-differential-amplifier` were repaired as the fourth
source-series batch.

Changes made:

- each task now has four negative variants: the original `neg_001_zero` plus
  three targeted behavior mutations;
- the new negatives cover clamp rails, gain and offset mistakes, differential
  polarity mistakes, mux selection mistakes, denominator safety mistakes,
  logarithm/floor mistakes, and soft-clamp shape mistakes;
- the absolute-value checker was made semantic (`sigout ~= abs(sigin)`) instead
  of being tied to one historical waveform, so both source absolute-value tasks
  are checked by behavior rather than by stale sample constants.

EVAS 0.4.5 local verification:

- 16/16 gold solutions PASS;
- 64/64 concrete negative variants fail behavioral correctness;
- no negative variant passed unexpectedly.

## Completed Batch: 128-143

Tasks `128-source-two-input-and-gate` through
`143-source-deadband-window` were repaired as the third source-series batch.

Changes made:

- each task now has four negative variants: the original `neg_001_zero` plus
  three targeted behavior mutations;
- the new negatives cover truth-table substitutions, threshold/edge mistakes,
  gain/scale mistakes, state-machine mistakes, and missing residue/deadband
  operations;
- weak candidate negatives that were hidden-test equivalent were replaced with
  distinguishable failures.

EVAS 0.4.5 local verification:

- 16/16 gold solutions PASS;
- 64/64 concrete negative variants fail behavioral correctness;
- no negative variant passed unexpectedly.
