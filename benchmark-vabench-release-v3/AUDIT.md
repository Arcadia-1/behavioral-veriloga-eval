# v3 Task Quality Audit

This file records durable public audit status for the v3 task set. It is not a
private Vela run log.

## Migrated Task Audit

As of 2026-06-26, v3 contains 185 migrated tasks. The initial migrated-task
audit found that most imported tasks had only one concrete negative
variant, usually `neg_001_zero`. That is not strong enough for the final
benchmark standard because it proves little beyond "not all outputs are zero."

The migrated-task repair is being done in batches. Each repaired batch should
meet these minimum conditions:

- public task contract and implementation boundary are clear;
- gold solution passes the EVAS checker through the normal task id path;
- each task has multiple concrete behavior negatives, not only all-zero;
- every new negative compiles and fails behavioral correctness rather than
  failing by syntax or missing files.

## Final Migrated Task Audit

As of 2026-06-26, the migrated-task repair covers all 185 migrated tasks
identified before the internal ID migration.

Current-state checks:

- 185/185 migrated tasks have the required public assets:
  `instruction.md`, `starter/`, `solution/`, `test_visible/`, `test_hidden/`,
  top-level `CHECKS.json` entries, and `negative_variants/manifest.json`;
- 185/185 migrated tasks use the v3-standard `variants/path` negative
  manifest shape;
- 185/185 migrated tasks have at least four concrete negative variants;
- no migrated task directory still uses the historical prefixed public directory name;
- no stale migrated-task `negative_cases.json` planned-negative file remains.

EVAS 0.4.5 local verification using the repository `.venv`:

- hidden/formal migrated-task sweep: 926/926 expected outcomes;
- 185/185 gold solutions PASS;
- 741/741 concrete negative variants fail behavioral correctness;
- 0 negative variants fail by DUT compile, testbench compile, timeout, or
  missing artifact;
- solver-visible smoke scripts: 185/185 PASS using only `starter/` and the
  public visible smoke testbench.

Follow-up fixes from the final sweep:

- `293-flash-folded-dac4` negative `neg_003_wrong_denominator` was rewritten
  from an EVAS tuple-triggering compressed expression into the same branch
  structure as the gold solution with only the denominator changed, so it now
  compiles and fails behavioral correctness;
- `079-jittered-clock-source-deterministic` visible smoke now forces the Python
  EVAS engine, matching the rest of the migrated-task visible smoke scripts.

## Completed Pilot: 288-300

Tasks `288-absolute-value` through
`300-pfd-active-low-reset` were used as the first migrated-task repair
pilot.

Changes made:

- each task now has four negative variants: the original `neg_001_zero` plus
  three targeted behavior mutations;
- `runners/simulate_evas.py` registers checker aliases for the task ids
  `v3_288_*` through `v3_300_*`, so the normal top-level task id path
  reaches the checker without requiring a manual `--checker-task-id` override.

EVAS 0.4.5 local verification:

- 13/13 gold solutions PASS;
- 52/52 concrete negative variants fail behavioral correctness;
- no negative variant passed unexpectedly.

## Completed Batch: 112-127

Tasks `112-clocked-sar-comparator` through
`127-sar-weighted-sum` were repaired as the second repair batch.

Changes made:

- each task now has four negative variants: the original `neg_001_zero` plus
  three targeted behavior mutations;
- task `123-start-gated-offset-search` gold was corrected so START is
  handled as an explicit enable transition instead of a continuous reset;
- source checker aliases now cover the normal top-level task ids for this batch.

EVAS 0.4.5 local verification:

- 16/16 gold solutions PASS;
- 64/64 concrete negative variants fail behavioral correctness;
- no negative variant passed unexpectedly.

## Completed Batch: 176-191

Tasks `176-dual-modulus-divider-16-17` through
`191-dac-8bit-ideal-scalar` were repaired as the sixth repair
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

Tasks `192-flash-data-align-pipeline` through
`207-iterative-isar-dac` were repaired as the seventh repair
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

## Completed Batch: 208-223

Tasks `208-offset-bisection-driver` through
`223-adc-sample-clock-sequencer` were repaired as the eighth
repair batch.

Changes made:

- each task now has four negative variants: the original `neg_001_zero` plus
  three targeted behavior mutations;
- the new negatives cover offset-bisection sign and step mistakes, weighted
  decoder normalization/output mistakes, toggle and DFF control mistakes,
  synchronization pipeline mistakes, progress encoder mistakes, TDC sign/scale
  mistakes, foreground calibration mistakes, pipeline alignment mistakes,
  mux-sampling mistakes, DAC code-generation mistakes, RDAC search-flow
  mistakes, SPI shift-direction mistakes, SAR-front-end clock/output mistakes,
  and ADC sample-clock sequencer output mistakes;
- weak candidate negatives that were not observed by the current hidden
  waveform were replaced with directly observable behavioral failures.

EVAS 0.4.5 local verification:

- 16/16 gold solutions PASS;
- 64/64 concrete negative variants fail behavioral correctness;
- no negative variant passed unexpectedly.

## Completed Batch: 224-239

Tasks `224-pipeline-counter-onehot` through
`239-l2-cdac-4b-switch` were repaired as the ninth repair batch.

Changes made:

- each task now has four negative variants: the original `neg_001_zero` plus
  three targeted behavior mutations;
- the new negatives cover counter modulus and edge mistakes, CDAC residue
  sign/weight/output mistakes, PFD reset and output polarity mistakes, trim
  code output mistakes, RDAC sweep output mistakes, SAR decision/reset/output
  mistakes, self-timed SAR step and comparator-clock mistakes, PFD reset-window
  mistakes, pipe-ADC gain-control mistakes, clock sequencer output mistakes,
  chopper gain/polarity mistakes, weighted ADC/DAC scale mistakes, quantizer
  threshold/level mistakes, and ready-gated DAC output mistakes;
- weak candidate negatives that were below tolerance or not exercised by the
  current hidden waveform were replaced with observable behavioral failures.

EVAS 0.4.5 local verification:

- 16/16 gold solutions PASS;
- 64/64 concrete negative variants fail behavioral correctness;
- no negative variant passed unexpectedly.

## Completed Batch: 240-255

Tasks `240-cdac-monodown-7b` through
`255-tool-4bit-sar-signed-dac` were repaired as the tenth repair
batch.

Changes made:

- each task now has four negative variants: the original `neg_001_zero` plus
  three targeted behavior mutations;
- the new negatives cover CDAC residue sign/weight/output mistakes, zoom timing
  sequencer output mistakes, 7-bit SAR/SAR2 decision and comparator-clock
  mistakes, DAC denominator/bipolar-offset/output-scale mistakes, offset-search
  step/polarity mistakes, comparator reset/output mistakes, sample-hold edge
  and tracking mistakes, signed SAR weighting mistakes, and readout/signed-DAC
  weight/gain/sample-edge mistakes;
- weak candidate negatives that were below tolerance were replaced with
  distinguishable output-level or weight failures.

EVAS 0.4.5 local verification:

- 16/16 gold solutions PASS;
- 64/64 concrete negative variants fail behavioral correctness;
- no negative variant passed unexpectedly.

## Completed Batch: 256-271

Tasks `256-dac4bit-small-swing` through
`271-coarse-qtz-3bit-residue` were repaired as the eleventh repair
batch.

Changes made:

- each task now has four negative variants: the original `neg_001_zero` plus
  three targeted behavior mutations;
- the new negatives cover DAC bipolar range, bit-weight, threshold, comparator
  reset/output/polarity, SAR readout weighting, serial accumulator reset/edge,
  SAR decoder count and normalization, one-shot trigger/width/turn-off, DFF
  async-control and complement output, PFD state/output behavior,
  sample-and-hold capture, trim/popcount encoding, and quantizer/residue
  mistakes;
- weak candidate negatives that the current hidden waveform did not observe
  were replaced with directly observable scale, count, state, or code-offset
  failures.

EVAS 0.4.5 local verification:

- 16/16 gold solutions PASS;
- 64/64 concrete negative variants fail behavioral correctness;
- no negative variant passed unexpectedly.

## Completed Batch: 272-282

Tasks `272-rs-phase-detector` through `282-pfd-timer-reset` were repaired as
the twelfth repair batch.

Changes made:

- each task now has four negative variants: the original `neg_001_zero` plus
  three targeted behavior mutations;
- the new negatives cover RS latch set/reset behavior, level-shift offset and
  gain mistakes, weighted decoder normalization/threshold mistakes,
  divide-by-two toggle state mistakes, modulo-8 accumulator pulse mistakes,
  XOR detector complement/FB mistakes, decision-router truth-table mistakes,
  safe-divider denominator guard mistakes, variable-gain differential polarity
  and clipping mistakes, programmable divider ratio/counter mistakes, and PFD
  delayed-reset/output-polarity mistakes;
- weak candidate negatives that were hidden-test equivalent were replaced with
  directly observable stuck-state, scale, threshold, or pulse-count failures;
- EVAS issue Arcadia-1/EVAS#17 was filed for the `V(node) - scalar` compile
  bug encountered during negative construction; the committed negative uses an
  equivalent parenthesized expression that compiles on EVAS 0.4.5.

EVAS 0.4.5 local verification:

- 11/11 gold solutions PASS;
- 44/44 concrete negative variants fail behavioral correctness;
- no negative variant passed unexpectedly.

## Completed Single: 079

Task `079-jittered-clock-source-deterministic` was normalized as the final
migrated task.

Changes made:

- the existing five concrete negative variants were preserved because all of
  them compile and fail behavioral correctness;
- `negative_variants/manifest.json` was converted from the old `cases/artifact`
  shape to the v3-standard `variants/path` shape used by the rest of the
  release;
- stale planned-negative metadata files were removed from the public task
  directory.

EVAS 0.4.5 local verification:

- 1/1 gold solution PASS;
- 5/5 concrete negative variants fail behavioral correctness;
- no negative variant passed unexpectedly.

## Completed Batch: 160-175

Tasks `160-voltage-controlled-gain-amplifier` through
`175-four-channel-edge-sampler` were repaired as the fifth repair
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

Tasks `144-differential-deadband` through
`159-variable-gain-differential-amplifier` were repaired as the fourth
repair batch.

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

Tasks `128-two-input-and-gate` through
`143-deadband-window` were repaired as the third repair batch.

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
