# Honest SOP Audit: Task 022 Bandgap Reference Macro Model

## Scope

Task boundary is one L1 Verilog-A DUT, `bandgap_reference_macro_model.va`. Public solver materials are `instruction.md`, `starter/`, and `test_visible/`. Evaluation materials are `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`.

## Gate 1

- Proposed label: `independent_l1_ready`.
- Reasoning: bandgap/reference startup behavior is a standalone bias/reference macro-model function, not a parameter-only variant of another row in this category.
- Human confirmation: confirmed by reviewer; retain as an independent L1 row for this category.

## Gate 2

- Status: `cadence_modeling_ready`.
- Public prompt now states the DUT boundary, interface, starter parameters, voltage-domain constraints, startup gating, line-regulated reference behavior, brownout reset, and valid metric.
- Visible and hidden decks are structurally distinct.
- Cadence/Verilog-A correspondence: the gold uses event-updated real state with `@(initial_step)`, `@(cross(...))`, and `transition()` on discrete target variables, matching the Cadence behavioral-modeling guidance for smoothed piecewise-constant outputs.

## Checker And Evidence

- Checker id: `v3_022_bandgap_reference_macro_model`.
- EVAS hidden gold: PASS.
- EVAS negative variants: 5/5 rejected.
- Spectre hidden gold: PASS.
- Spectre negative variants: not rerun for this legacy nested-negative layout.
- EVAS lint preflight: PASS, 0 diagnostics.
- Cadence AHDL lint: PASS with no task-specific `AHDLLINT-*`; only global `VACOMP-2435` environment notice observed.

## Remaining Risk

Spectre negative coverage can be added later by normalizing the legacy nested negative layout, but current gold, EVAS negatives, Spectre hidden gold, and AHDL lint evidence support the task as an L1 category candidate.
