# Two-Gate SOP Audit: Task 263 Clocked Comparator Dual Output

## Scope

Task 263 is a reset-low clocked comparator DUT with complementary `outp/outn`
outputs. It latches a comparison on rising clock edges and resets both outputs
low on falling clock edges after the comparator delay.

This is a single-component L1 artifact, not a composed L2 flow.

## Gate 1: Admission And Counting

- Admission label: `independent_l1_ready` as the preferred reset-low
  complementary-output comparator representative, or
  `valid_variant_needs_counting_policy` if upstream maps reset-low coverage to
  another existing row.
- Counting decision: under the strict reset-family dedupe policy, task 263 is
  the strongest comparator-category reset-low representative because the prompt
  directly states complementary outputs and both reset/decision phases.
- Function boundary: reset-low clocked comparator with complementary outputs.
- Checker alignment: the checker verifies reset-low behavior, complementary
  positive/negative decisions, equal-input clearing, and swapped-output
  negatives.

## Gate 2: Cadence Modeling Quality

- Modeling status: `cadence_modeling_ready` after bridge-backed Spectre gold
  and negative validation. The result JSON reports no task-level errors; the
  remaining Spectre warnings are global AHDL-CMI/environment or simulator-mode
  notices rather than task-specific Verilog-A modeling findings.
- Prompt hygiene: the prompt now states the public interface, clock/reset edge
  behavior, delay, rail-derived outputs, and constraints without source-import
  wording.
- Metadata repair: `TASKS.json` now classifies this single-component DUT as L1,
  and release-level `CHECKS.yaml` includes a current `sim_correct:` block.
- Counting risk: if the final release uses another reset-low comparator as the
  canonical row, keep task 263 as a valid non-counted variant.

## Evidence

- EVAS hidden gold: PASS; the checker reports three decisions, three reset
  windows, and positive/negative/equal-input coverage.
- EVAS negatives: 4/4 behavioral rejections covering zero output, missing
  falling reset, inverted comparison, and swapped complementary outputs.
- Spectre hidden gold: PASS via the restored Virtuoso bridge
  (`BRIDGE_PROFILE=jin`, `--spectre-backend bridge`).
- Spectre negatives: 4/4 `NEGATIVE_REJECTED` on the hidden deck. The completed
  bridge rerun rejects zero output, missing falling reset, inverted comparison,
  and swapped complementary outputs.

## Human Confirmation

The reviewer confirmed that reset-family dedupe should be strict, but that a
representative reset-low complementary-output comparator is useful benchmark
coverage.
