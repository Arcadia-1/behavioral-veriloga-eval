# Behavioral Verilog-A v3

This directory is a clean, RTL-Forge-style packaging of 494 Verilog-A
DUT/support/testbench/e2e and language-extension tasks.

The first 300 tasks remain the original behavior-certified full-300 surface.
Tasks `301`-`494` are LRM/course-material extension candidates. They are
compile-supported language rows unless promoted by layer-specific behavior
evidence; they are not part of the original full-300 behavior claim.

Top-level indexes:

- `TASKS.json`: canonical task ids, titles, forms, directories, and target
  Verilog-A artifacts for all tasks.
- `CHECKS.yaml`: canonical checker configuration for all tasks, replacing
  per-task `test_harness/checks.yaml` files.
- `reports/layered_certification.json`: machine-readable certification-layer
  boundary for the 300 certified rows and 194 extension candidates.
- `reports/layered_certification.md`: human-readable version of the layered
  certification summary.

Partitions:

- `001`-`049`: migrated v1 DUT tasks.
- `050`-`079`: testbench utility / Verilog-A helper module tasks.
- `080`-`089`: additional migrated DUT/support modules from v1.
- `090`-`111`: additional useful Verilog-A module tasks promoted into v3.
- `112`-`300`: imported and repaired DUT/module tasks, including the obsolete
  v2 five-task slice absorbed as normal v3 tasks.
- `301`-`494`: Verilog-A / Verilog-AMS language extension candidates covering
  functions/tasks, file I/O, table models, random/noise helpers, AMS digital
  syntax, Cadence LRM helper calls, continuous-time operators, and KCL syntax.

Each task is self-contained under `tasks/NNN-name/`:

- `instruction.md`: the problem statement the agent sees.
- `starter/`: files the agent edits.
- `test_visible/`: public smoke tests the agent may run.
- `test_hidden/`: hidden testbenches for grading.
- `test_harness/`: evaluation bridge files.
- `solution/`: golden reference implementation.
- `negative_variants/`: intentionally wrong implementations used to audit checker strength.

The agent-facing surface is intentionally small: `instruction.md`, `starter/`,
and `test_visible/`. Hidden tests, checker configs in `CHECKS.yaml`, golden
solutions, and negative variants are evaluator-side material.

Task names describe the circuit/helper being built instead of preserving legacy migration ids. Private submission records, image tags, model ids, and other orchestration state remain outside this public benchmark tree.

## EVAS Lint Preflight

Use `scripts/run_v3_evas_lint_preflight.py` from the repository root to run the
EVAS AHDL-like linter over staged v3 gold or starter cases before promotion or
manual review. By default it stages solution artifacts with hidden testbenches,
runs `evas lint`, and fails only on EVAS/Spectre compatibility errors; AHDL-like
warnings remain review signals.

Example:

```bash
python3 scripts/run_v3_evas_lint_preflight.py --tasks 049,284 --split hidden --out scratch/v3_lint_probe.json
```

Write lint output to scratch/generated locations. Do not commit generated lint,
certification, simulator, or private oracle reports into the public benchmark
tree.
