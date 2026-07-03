# Behavioral Verilog-A v3

This directory is a clean, RTL-Forge-style packaging of 451 numbered
standalone-Spectre-compatible Verilog-A DUT/support/testbench/e2e and
language-extension tasks, plus five unnumbered replacement candidates.

The default `tasks/` tree is the Spectre-compatible denominator. Task numbers
are not contiguous: 54 rows that standalone Cadence/Spectre rejects as written
were moved to `spectre-unsupported-tasks/` and removed from `TASKS.json` and
`CHECKS.yaml`. Those rows are archived for future AMS/digital or version-gated
work, but they are not part of the default EVAS/Spectre parity score.

Rows `001`-`300` remain the original behavior-certified surface except for
seven converter/vector rows (`052`-`057`, `075`) that used procedural vector
indexing patterns rejected by Spectre. Rows `301+` are LRM/course-material
extension candidates unless promoted by layer-specific behavior evidence.

Top-level indexes:

- `TASKS.json`: canonical task ids, titles, forms, directories, and target
  Verilog-A artifacts for all tasks.
- `CHECKS.yaml`: canonical checker configuration for all tasks, replacing
  per-task `test_harness/checks.yaml` files.
- `reports/layered_certification.json`: machine-readable certification-layer
  boundary for the current Spectre-compatible default denominator.
- `reports/layered_certification.md`: human-readable version of the layered
  certification summary.
- `reports/spectre_unsupported_removed_20260703.{json,md}`: archived-row list
  and reasons for removing 54 Spectre-rejected rows from the default
  denominator.
- `reports/spectre_default_after_removal_20260703.{json,md}`: hidden-gold
  Spectre audit over the retained 451-row default denominator.

Partitions:

- `001`-`049`: migrated v1 DUT tasks.
- `050`-`079`: testbench utility / Verilog-A helper module tasks.
- `080`-`089`: additional migrated DUT/support modules from v1.
- `090`-`111`: additional useful Verilog-A module tasks promoted into v3.
- `112`-`300`: imported and repaired DUT/module tasks, including the obsolete
  v2 five-task slice absorbed as normal v3 tasks.
- `301`-`505`: Verilog-A language extension candidates covering functions,
  file I/O, table models, random/noise helpers, Cadence LRM helper calls,
  continuous-time operators, and KCL syntax, with Spectre-rejected AMS/digital,
  user-task, and unsupported vector/helper rows archived outside `tasks/`.

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
