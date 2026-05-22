# behavioral-veriloga-eval

This repository holds the vaBench benchmark source, EVAS/Spectre validation
runners, schemas, gold assets, and compact evidence reports.

Current mainline:

```text
vaEVAS = vaBench benchmark + EVAS Spectre-aligned fast evaluator
```

## Current Entrypoints

- `docs/VAEVAS_MAINLINE_PLAN.md`: project plan and work order.
- `docs/VABENCH_TOPDOWN_FUNCTION_TAXONOMY.md`: function taxonomy for building a
  complete benchmark, independent of historical construction artifacts.
- `docs/VABENCH_MAIN120_MATERIALIZATION.*`: source-task materialization status.
- `docs/VABENCH_D004_BUGFIX_TRIAGE.md`: bugfix provenance and release policy.
- `docs/VAEVAS_VALIDATION_PIPELINE.md`: validation route and promotion gates.
- `docs/EVAS_SPECTRE_CONFORMANCE_BACKLOG.md`: isolated EVAS/Spectre conformance
  regression backlog.

## Benchmark Shape

Each release-quality task should contain:

- `prompt.md`
- `meta.json`
- `checks.yaml`
- `gold/` assets when the task includes a reference implementation or testbench
- compact EVAS/Spectre evidence links for paper-facing claims

The four normal task families are:

- `spec-to-va`
- `tb-generation`
- `end-to-end`
- `bugfix`

EVAS/Spectre conformance cases are maintained separately from normal vaBench
task counts so simulator-semantics regressions do not masquerade as model
generation tasks.

## Validation

Use EVAS as the fast local evaluator and debugger. Use Spectre as the final
judge for gold promotion and paper-facing parity claims.

For benchmark changes, prefer:

1. static/source integrity checks
2. EVAS gold validation for changed tasks
3. Spectre or dual EVAS/Spectre validation for promoted/paper-facing evidence

Raw `results/` payloads, generated candidates, waveform dumps, and old workflow
sweeps are local/disposable unless promoted to a named fixture or compact report.
