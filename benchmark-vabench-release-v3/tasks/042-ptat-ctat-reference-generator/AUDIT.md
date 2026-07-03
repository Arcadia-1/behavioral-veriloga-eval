# Honest SOP Audit: Task 042 PTAT/CTAT Reference Generator

## Scope

Task boundary is one L1 Verilog-A DUT, `ptat_ctat_reference_generator.va`. Public solver materials are `instruction.md`, `starter/`, and `test_visible/`. Evaluation materials are `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`.

## Gate 1

- Proposed label: `independent_l1_ready`.
- Reasoning: PTAT/CTAT compensation is a distinct reference-generation behavior from bandgap startup gating, LDO regulation, POR, UVLO, and bias trim rows.
- Human confirmation: confirmed by reviewer; retain as an independent L1 row for this category.

## Gate 2

- Status: `cadence_modeling_ready`.
- Public prompt now states the DUT boundary, interface, starter parameters, normalized temperature/control input, PTAT metric, CTAT compensation, bounded reference output, and voltage-domain constraints.
- Visible and hidden decks are structurally distinct.
- Cadence/Verilog-A correspondence: the gold uses event-updated real branch abstractions and `transition()` on discrete target variables, matching Cadence-style behavioral reference modeling at the voltage-macro level.

## Checker And Evidence

- Checker id: `v3_042_ptat_ctat_reference_generator`.
- EVAS hidden gold: PASS.
- EVAS negative variants: 5/5 rejected.
- Spectre hidden gold: PASS.
- Spectre negative variants: not rerun for this legacy nested-negative layout.
- EVAS lint preflight: PASS, 0 diagnostics.
- Cadence AHDL lint: PASS with no task-specific `AHDLLINT-*`; only global `VACOMP-2435` environment notice observed.

## Remaining Risk

Spectre negative coverage can be added later by normalizing the legacy nested negative layout, but current gold, EVAS negatives, Spectre hidden gold, and AHDL lint evidence support the task as an L1 category candidate.
