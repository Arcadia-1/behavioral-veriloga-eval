# Two-Gate SOP Audit: Task 116 Clocked Comparator Reset-Low

## Scope

Task 116 is a reset-low clocked comparator DUT. It compares `VINP/VINN` on
`CMPCK` rising edges and resets both decision outputs low when `CMPCK` falls.

## Gate 1: Admission And Counting

- Admission label: `hard_duplicate_rewrite_or_remove`.
- Counting decision: human review confirmed that reset-low clocked comparator
  rows should be deduplicated strictly. Task 116 is valid modeled behavior, but
  it is functionally covered by the retained reset-low representative
  `263-clocked-comparator-dual-output`.
- Function boundary: reset-low clocked comparator with complementary decision
  outputs.
- Rewrite path: keep only if upstream wants a different reset-low interface
  role, such as explicit latch-valid signaling, metastability modeling, or a
  converter-front-end contract that is not already covered by task 263.

## Gate 2: Cadence Modeling Quality

- Modeling status: `cadence_modeling_ready` for the artifact itself, but not a
  separate counted function under the strict duplicate policy.
- Prompt hygiene: repaired to remove source-provenance and hidden-evaluator
  wording. The public prompt now states interface, parameters, edge behavior,
  delay, output smoothing, and voltage-only constraints.
- Checker coverage: `v3_clocked_comparator_reset_low` verifies reset-low
  behavior, positive and negative decisions, equal-input clearing, and
  behavioral negative variants.

## Human Confirmation

The reviewer confirmed that parameter, naming, or reset-family variants should
not become independent benchmark functions unless they add a distinct reusable
AMS role.
