# vaEVAS Concrete Experiment Runbook

**Date**: 2026-05-13

## Claim Map

| Claim | Why It Matters | Minimum Convincing Evidence | Experiment Blocks |
| --- | --- | --- | --- |
| C1: `vaBench` is a credible Verilog-A benchmark asset. | The paper needs a durable contribution independent of transient agent workflow choices. | Source-controlled tasks have complete prompts, metadata, checks, gold assets, and EVAS/Spectre evidence. | B1, B2, B5 |
| C2: EVAS is a fast, debuggable evaluator aligned with Spectre on the supported subset. | The simulator is useful only if it predicts Spectre pass/fail and exposes actionable failures faster. | Broad benchmark parity has zero EVAS PASS / Spectre FAIL mismatches, and known mismatches are reduced to atomic regressions. | B3, B4, B6 |
| Anti-claim: workflow/controller/RAG/SFT is the contribution. | Those layers are easy to overfit and likely to be replaced by stronger base models. | Baselines are simple stress users of the benchmark and evaluator, not paper-core mechanisms. | B7 |

## Experiment Blocks

### B1: Benchmark Source Materialization

- **Claim tested**: C1.
- **Why this block exists**: Current source-controlled `tasks/` has 92 gold-backed tasks, while `vabench-main-v1-main120` is currently local result evidence under `results/`.
- **Dataset / split / task**: `tasks/` plus the historical `vabench-main-v1-main120` result directories.
- **Compared systems**: none.
- **Metrics**: task count, family/category coverage, required file completeness, gold DUT/TB presence, provenance of each task.
- **Setup details**: restore or materialize the 120-task source split; keep `benchmark-vabench-main-v1/` out of docs unless the directory is actually restored.
- **Success criterion**: every main benchmark item maps to an editable task source and has a stable ID, metadata, checker, gold DUT, gold testbench, EVAS result, and Spectre result.
- **Failure interpretation**: if main120 cannot be materialized, the paper-facing benchmark must be scoped to the 92 tracked tasks until the missing 28 are restored.
- **Table / figure target**: benchmark inventory table.
- **Priority**: MUST-RUN.

### B2: Static Integrity and EVAS Gold Gate

- **Claim tested**: C1 and C2.
- **Why this block exists**: Benchmark expansion is meaningless unless each task is mechanically valid and EVAS-runnable.
- **Dataset / split / task**: all source-controlled benchmark tasks and each new expansion batch.
- **Compared systems**: EVAS only.
- **Metrics**: metadata schema pass rate, check determinism, EVAS binary pass rate, failure taxonomy.
- **Setup details**:
  - `python3 -m pytest -q tests/test_bridge_preflight.py tests/test_bridge_scripts.py tests/test_run_gold_dual_suite.py tests/test_save_statements.py tests/test_pwl_statements.py tests/test_meta_schema.py`
  - `python3 runners/run_gold_suite.py --task-root tasks --output-root results/<run-id>-evas`
- **Success criterion**: 100% metadata/checker integrity and no unexplained EVAS gold failure.
- **Failure interpretation**: integrity failures block promotion; EVAS gold failures become EVAS bug or task bug triage.
- **Table / figure target**: validation pipeline table.
- **Priority**: MUST-RUN.

### B3: Broad EVAS/Spectre Parity Gate

- **Claim tested**: C2.
- **Why this block exists**: The evaluator claim must be defended on realistic benchmark tasks, not only on small regressions.
- **Dataset / split / task**: current tracked tasks plus materialized main120 once available.
- **Compared systems**: EVAS vs Spectre on gold DUT/TB.
- **Metrics**: binary pass/fail agreement, EVAS PASS / Spectre FAIL count, Spectre PASS / EVAS FAIL count, per-axis pass rates, status-label mismatch count, runtime.
- **Setup details**:
  - `./scripts/run_with_bridge.sh python3 runners/run_gold_dual_suite.py --output-root results/<run-id>-dual`
  - run family slices first, then full main split.
- **Success criterion**: zero EVAS PASS / Spectre FAIL binary mismatches on audited gold slices; all status-label mismatches are either fixed or documented as taxonomy-only.
- **Failure interpretation**: EVAS false positives block evaluator claims; Spectre false positives usually indicate EVAS strictness or task/checker issues.
- **Table / figure target**: EVAS/Spectre parity table.
- **Priority**: MUST-RUN.

### B4: Atomic EVAS/Spectre Conformance Pack

- **Claim tested**: C2.
- **Why this block exists**: Broad parity failures couple multiple causes; conformance tests isolate one simulator semantic per case.
- **Dataset / split / task**: dedicated conformance directory or tracked regression tasks.
- **Compared systems**: EVAS parser/preflight/runtime vs Spectre.
- **Metrics**: compile legality agreement, runtime waveform agreement, event count agreement, diagnostic label agreement.
- **Setup details**: create one regression each for:
  - empty control branch syntax legality,
  - uncontinued multiline source/PWL syntax legality,
  - `$abstime` continuous decay sampling behavior,
  - status-label mismatches that do not change binary pass/fail.
- **Success criterion**: each historical EVAS PASS / Spectre FAIL class has a single-cause regression or a documented out-of-scope reason.
- **Failure interpretation**: remaining mismatch becomes an EVAS bug, Spectre policy note, or benchmark task bug.
- **Table / figure target**: conformance backlog table and appendix examples.
- **Priority**: MUST-RUN.

### B5: Benchmark Expansion Toward 200 Tasks

- **Claim tested**: C1.
- **Why this block exists**: The first public benchmark should cover standard circuit behavior broadly enough to be useful.
- **Dataset / split / task**: new batches of 20-40 tasks.
- **Compared systems**: none at creation time; EVAS/Spectre after gold validation.
- **Metrics**: coverage by circuit family, abstraction level, language construct, checker type, difficulty, and validation status.
- **Setup details**: prioritize four layers:
  - primitive Verilog-A semantics and syntax,
  - analog functional blocks,
  - mixed-signal behavioral blocks,
  - small system-level standard circuits.
- **Success criterion**: each batch passes static checks, EVAS gold, Spectre gold, and a short manual review note before promotion.
- **Failure interpretation**: failed tasks stay in staging, not main.
- **Table / figure target**: benchmark coverage figure.
- **Priority**: MUST-RUN after B1-B4 are stable.

### B6: EVAS Speed and Debug Evidence

- **Claim tested**: C2.
- **Why this block exists**: EVAS must be more than a Spectre wrapper; its value is fast feedback and debuggability.
- **Dataset / split / task**: representative slices from primitive, block, mixed-signal, and system tasks.
- **Compared systems**: EVAS vs Spectre.
- **Metrics**: wall-clock runtime, failure localization quality, log size, first-actionable-error availability.
- **Setup details**: run EVAS and Spectre on the same gold tasks; capture timing and diagnostic artifacts.
- **Success criterion**: EVAS is consistently faster on supported tasks and reports failure locations that are useful for repair/debug.
- **Failure interpretation**: if speedup is small, keep the claim focused on debug and validation workflow instead of raw performance.
- **Table / figure target**: speed/debug table.
- **Priority**: MUST-RUN for paper packaging.

### B7: Minimal Model Baselines

- **Claim tested**: Anti-claim only.
- **Why this block exists**: Models are benchmark users, not the core contribution.
- **Dataset / split / task**: stable main benchmark after B1-B4.
- **Compared systems**: prompt-only, EVAS-feedback, optional Spectre-feedback.
- **Metrics**: task pass rate, compile pass rate, behavior pass rate, EVAS/Spectre agreement on generated candidates, token/runtime cost.
- **Setup details**: keep the loop simple; no custom controller claim, no SFT until benchmark/evaluator evidence is stable.
- **Success criterion**: model rows show the benchmark is nontrivial and EVAS feedback is useful, without shifting the paper to workflow optimization.
- **Failure interpretation**: weak baselines are acceptable if the benchmark/evaluator claim is strong.
- **Table / figure target**: small baseline table or appendix.
- **Priority**: NICE-TO-HAVE.

## Run Order

| Milestone | Goal | Runs | Decision Gate | Cost | Risk |
| --- | --- | --- | --- | --- | --- |
| M0 | Verify bridge and local validation readiness. | R001-R004 | Bridge package imports, tests pass, Spectre license/smoke works. | Low | Persistent tunnel is currently unstable. |
| M1 | Materialize benchmark source. | R005-R007 | main benchmark has source-backed task IDs and no missing gold assets. | Medium | Missing 28 main120 tasks may require reconstruction. |
| M2 | Lock EVAS-only validity. | R008-R010 | all tracked gold tasks pass integrity and EVAS gold checks. | Low-medium | Checker drift can look like simulator failure. |
| M3 | Run broad EVAS/Spectre parity. | R011-R014 | zero EVAS PASS / Spectre FAIL mismatches on audited gold slices. | Medium-high | Spectre bridge availability and runtime. |
| M4 | Build conformance pack. | R015-R020 | historical mismatch classes are atomic regressions. | Medium | Some historical failures may be out of current scope. |
| M5 | Expand benchmark. | R021-R024 | each batch has validation and coverage deltas. | Medium | Manual review bottleneck. |
| M6 | Package paper evidence. | R025-R028 | tables and figures trace to fresh artifacts. | Low-medium | Claims may overstate current evidence. |

## Current Bridge Update Evidence

- Updated `/Users/bucketsran/Documents/TsingProject/iccad/virtuoso-bridge-lite` from `9a04421` to `02d4264`.
- Refreshed editable install from `virtuoso-bridge==0.1.0` to `virtuoso-bridge==0.7.0`.
- Added Python 3.9 compatibility imports to `maestro/lifecycle.py` and `maestro/writer.py`.
- `python -m pytest` in bridge repo: 31 passed.
- Direct SSH Spectre license probe: OK, Spectre path `/home/cadence/spectre/SPECTRE211Hotfix/tools/bin/spectre`, version `21.1.0`.
- Direct SSH Spectre RC smoke: `ok=True`, downloaded PSFASCII artifacts and parsed DC/AC signals.
- Bridge-managed persistent tunnel is still unstable: `virtuoso-bridge start` can probe Spectre, but follow-up `status`/`license` sees no managed tunnel listener.

## Stop Conditions

- Stop benchmark promotion when any task lacks source, metadata, checks, gold DUT/TB, EVAS result, or Spectre result.
- Stop evaluator claims when any in-scope EVAS PASS / Spectre FAIL mismatch remains unexplained.
- Stop workflow/model work when it starts requiring custom controller or SFT claims before benchmark and EVAS evidence are stable.
