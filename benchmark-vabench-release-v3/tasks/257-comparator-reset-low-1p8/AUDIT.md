# Two-Gate SOP Audit: Task 257 Comparator Reset-Low 1.8 V

## Scope

Task 257 is a clocked comparator DUT in a 1.8 V output domain. It compares
`vinp/vinn` on `cmpck` rising edges and resets both outputs low when `cmpck`
falls.

This is a single-component L1 artifact, not a composed L2 flow.

## Gate 1: Admission And Counting

- Admission label: `valid_variant_needs_counting_policy`.
- Counting decision: task 257 is a valid reset-low clocked-comparator artifact,
  but the 1.8 V rail and default timing alone do not make a separate
  independent benchmark. Human review confirmed task
  `263-clocked-comparator-dual-output` as the retained reset-low representative.
- Function boundary: reset-low clocked comparator with rail-derived output
  levels.
- Checker alignment: the checker verifies reset-low behavior, decision
  polarity after rising edges, swapped-output negatives, and 1.8 V output
  scaling.

## Gate 2: Cadence Modeling Quality

- Modeling status: `cadence_modeling_ready` after prompt/schema repair and
  current comparator-batch EVAS/Spectre validation.
- Prompt hygiene: the prompt now states the public interface, 1.8 V output
  domain, reset/decision behavior, and modeling constraints without
  source-import wording.
- Metadata repair: `TASKS.json` now classifies this single-component DUT as L1,
  and release-level `CHECKS.yaml` includes a current `sim_correct:` block.
- Counting risk: keep only as a non-counted rail-domain variant or rewrite
  candidate unless upstream explicitly wants a separate supply-domain comparator
  row.

## Human Confirmation

The reviewer confirmed strict duplicate handling for clocked comparator reset
families; different rails or delay defaults need a stronger functional reason
before becoming independent counted coverage.
