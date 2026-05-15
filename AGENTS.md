# Repository Guidelines

## Current vaEVAS Mainline
This repository exists to support the paper-facing vaEVAS mainline:

> **vaEVAS = vaBench benchmark + EVAS Spectre-aligned fast evaluator.**

Benchmark construction and EVAS/Spectre parity are the durable contributions. LLM repair loops, controllers, RAG, compile skills, prompt variants, token optimization, and local/SFT model experiments are support harnesses only; do not treat them as the core research direction unless the user explicitly reopens that scope.

Default priorities:
- Strengthen the tracked `tasks/` benchmark tree, the `vabench-main-v1-main120` evidence asset, future vaBench splits, gold references, checkers, schemas, and coverage metadata.
- Preserve and extend EVAS/Spectre parity evidence and regression cases.
- Keep Spectre as the final paper-facing judge; use strict EVAS as a fast filter/debug evaluator.
- Avoid benchmark memorization, local model fine-tuning, and workflow over-optimization as default investments.
- Keep generated candidates, raw simulator outputs, waveform dumps, and historical workflow sweeps out of versioned or high-signal paths unless promoted to a named fixture/report.

Benchmark/evaluator split policy:
- `vaBench-main` should be the broad end-to-end benchmark and can be used directly for EVAS/Spectre parity audits.
- In the current worktree, the source-controlled benchmark source is `tasks/`; the historical `benchmark-vabench-main-v1` directory is not present, while `vabench-main-v1-main120` appears as local result evidence under `results/`.
- Use `docs/VABENCH_MAIN120_MATERIALIZATION.md` and `runners/materialize_main120_inventory.py` as the provenance surface for main120 source recovery. Do not frame the work as "92 existing plus 28 missing"; current `tasks/` and main120 have different task ID sets.
- Separate EVAS/Spectre conformance regressions are still useful because they isolate one failure cause per case: Spectre syntax legality, source parsing, event scheduling, solver-time sampling, waveform breakpoint behavior, or checker semantics.
- "Small and focused" means each parity regression is atomic and diagnostic, not that the suite must stay tiny. Add as many dedicated EVAS/Spectre stress cases as needed when they cover distinct semantics.
- Heldout splits are optional future leaderboard/generalization assets. Do not prioritize heldout construction ahead of main benchmark coverage, gold validation, and EVAS/Spectre parity.

## Project Structure & Module Organization
`tasks/` holds benchmark cases, organized as `tasks/<family>/voltage/<category>/<case>/` with `prompt.md`, `meta.json`, `checks.yaml`, and optional `gold/`. `examples/` contains runnable reference designs, grouped by intent such as `digital-logic/`, `data-converter/`, and `stimulus/`; each example usually includes `.va`, `tb_*.scs`, `analyze_*.py`, and `validate_*.py` files. `runners/` contains harness scripts for migration and EVAS execution. `schemas/` defines the task and result JSON formats.

## Build, Test, and Development Commands
Use `python3` for repository tooling.

- `python3 runners/run_examples_suite.py --output-root results/examples-suite` - runs the manifest-driven smoke suite for the example library.
- `python3 runners/simulate_evas.py tasks/end-to-end/voltage/clk_div_smoke examples/digital-logic/clk_div/clk_div.va examples/digital-logic/clk_div/tb_clk_div.scs` - executes one DUT/testbench pair through EVAS.
- `python3 examples/digital-logic/clk_div/validate_clk_div.py` - runs a case-specific validation script when present.
- `python3 runners/migrate_veriloga_evals.py` - regenerates structured task directories from the legacy eval list; only use when the upstream source repo is available.

## Coding Style & Naming Conventions
Follow existing Python style: 4-space indentation, type hints where helpful, and small single-purpose functions. Use `snake_case` for Python files, functions, task IDs, and JSON keys. Keep Verilog-A modules descriptive and lowercase with underscores, for example `clk_div.va`. Prefix Spectre testbenches with `tb_`, analysis helpers with `analyze_`, and check scripts with `validate_`. Match the current formatting in JSON and YAML files; no formatter configuration is committed here, so keep diffs minimal and consistent.

## Testing Guidelines
There is no centralized `tests/` package yet; validation is case-driven. For benchmark content changes, run the nearest `validate_*.py` script and, when applicable, the full examples smoke suite. Preserve the executable scoring axes used across the repo: `dut_compile`, `tb_compile`, and `sim_correct`. When adding a new task, ensure `meta.json` and `checks.yaml` stay aligned with `schemas/`.

## Commit & Pull Request Guidelines
History is currently minimal (`Initial commit`), so use short imperative commit subjects such as `Add SAR logic voltage task`. Keep commits focused on one task family or runner change. Pull requests should describe the affected paths, note any EVAS or validation commands you ran, and include sample output or result snippets when behavior changes. Link related issues or benchmark gaps when available.

## Environment & Safety Notes
This repository is EVAS-focused and intentionally limited to pure voltage-domain Verilog-A flows. Avoid introducing current-domain checks unless the benchmark scope changes. Do not commit generated result directories or simulator artifacts unless they are intentional fixtures.
