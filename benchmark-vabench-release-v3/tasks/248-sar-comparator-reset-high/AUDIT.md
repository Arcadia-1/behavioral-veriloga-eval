# Two-Gate SOP Audit: Task 248 SAR Comparator Reset-High

## Scope

Task 248 is a clocked SAR-style comparator DUT. It compares `vinp/vinn` on
`cmpck` rising edges and resets both differential outputs high when `cmpck`
falls.

This is a single-component L1 artifact, not a composed L2 flow.

## Gate 1: Admission And Counting

- Admission label: `valid_variant_needs_counting_policy`.
- Counting decision: task 248 is a valid reset-high clocked-comparator artifact
  but overlaps with existing reset-high SAR/comparator coverage. Human review
  confirmed that reset-family rows should be deduplicated strictly, and task
  `112-clocked-sar-comparator` is the retained reset-high representative unless
  upstream explicitly chooses task 248 instead.
- Function boundary: SAR-facing reset-high clocked comparator with
  complementary decision outputs.
- Checker alignment: the checker verifies reset-high behavior, decision
  polarity after rising edges, and rail-derived output levels.

## Gate 2: Cadence Modeling Quality

- Modeling status: `cadence_modeling_ready` after prompt/schema repair and
  current comparator-batch EVAS/Spectre validation.
- Prompt hygiene: the prompt now exposes public interface, reset behavior,
  output timing, and constraints without source-import wording.
- Metadata repair: `TASKS.json` now classifies this single-component DUT as L1,
  and release-level `CHECKS.yaml` includes a current `sim_correct:` block.
- Counting risk: retain only as a non-counted reset-high variant or rewrite
  candidate unless upstream selects it as the canonical reset-high
  SAR-comparator representative.

## Human Confirmation

The reviewer confirmed that small timing/default differences are not enough to
make this a separate independent function when the reset-high clocked
comparator role is already represented.
