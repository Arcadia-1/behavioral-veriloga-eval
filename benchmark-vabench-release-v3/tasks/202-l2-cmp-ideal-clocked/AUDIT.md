# Two-Gate SOP Audit: Task 202 Clocked Comparator Reset-High Variant

## Scope

Task 202 implements a single clocked comparator DUT. When `cmpck` is low, both
outputs reset high; after a rising clock edge, `dcmpp/dcmpn` report the
latched comparison of `vinp` and `vinn` after the comparator delay.

Despite the historical task name, this is a single-component L1 artifact, not a
composed L2 flow.

## Gate 1: Admission And Counting

- Admission label: `valid_variant_needs_counting_policy`.
- Counting decision: human review confirmed that clocked-comparator reset
  variants should be deduplicated strictly. Task 202 is a valid modeled
  artifact, but reset polarity, naming, and a small delay/default difference
  are not enough by themselves to make another independent counted benchmark.
  Task `112-clocked-sar-comparator` is the retained reset-high representative
  unless upstream explicitly chooses a different reset-high row.
- Function boundary: reset-high clocked comparator with complementary outputs.
- Checker alignment: the checker verifies reset-high behavior, positive and
  negative decisions after rising edges, equal-input behavior, and output rails.

## Gate 2: Cadence Modeling Quality

- Modeling status: `cadence_modeling_rework` for counted use. The artifact
  prompt is repaired, but the visible and hidden SCS decks are currently
  byte-identical, so this row does not have robust private coverage.
- Prompt hygiene: the prompt now states the public interface, parameters,
  reset/decision semantics, and modeling constraints without source-import or
  hidden-evaluator wording.
- Metadata repair: release-level `CHECKS.yaml` now includes a current
  `sim_correct:` block, so the default gold/negative verifier no longer skips
  this row.
- Counting risk: retain only as a non-counted variant or rewrite candidate.
  If upstream chooses this row as the canonical reset-high
  clocked-comparator representative instead of task 112, repair the hidden deck
  and rerun EVAS/Spectre before counting it.

## Human Confirmation

The reviewer confirmed that this reset-family row should be judged under the
strict duplicate policy: different naming, default delay, or reset-family
surface variation is not sufficient independent function coverage by itself.
