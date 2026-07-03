# Honest SOP Audit: Task 038 Power-On Reset Detector

## Scope

Task boundary is one L1 Verilog-A DUT, `power_on_reset_detector.va`. Public solver materials are `instruction.md`, `starter/`, and `test_visible/`. Evaluation materials are `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`.

## Gate 1

- Proposed label: `independent_l1_ready`.
- Reasoning: active-high power-on reset with supply thresholding, clocked release delay, and brownout reassertion is an independent power-management detector. It is distinct from UVLO/power-good hysteresis in task 048.
- Human confirmation: confirmed by reviewer; retain as an independent L1 row for this category.

## Gate 2

- Status: `cadence_modeling_ready`.
- Public prompt now states the DUT boundary, interface, starter parameters, active-high reset polarity, supply-good threshold, release-delay behavior, brownout behavior, and metric semantics.
- Visible and hidden decks are structurally distinct.
- Cadence/Verilog-A correspondence: the gold uses event-updated state and counters with `@(initial_step)`, `@(cross(...))`, and `transition()` on discrete target variables, matching Cadence-style event-driven behavioral models.

## Checker And Evidence

- Checker id: `v3_038_power_on_reset_detector`.
- EVAS hidden gold: PASS.
- EVAS negative variants: 5/5 rejected.
- Spectre hidden gold: PASS.
- Spectre negative variants: not rerun for this legacy nested-negative layout.
- EVAS lint preflight: PASS, 0 diagnostics.
- Cadence AHDL lint: PASS with no task-specific `AHDLLINT-*`; only global `VACOMP-2435` environment notice observed.

## Remaining Risk

Spectre negative coverage can be added later by normalizing the legacy nested negative layout, but current gold, EVAS negatives, Spectre hidden gold, and AHDL lint evidence support the task as an L1 category candidate.
