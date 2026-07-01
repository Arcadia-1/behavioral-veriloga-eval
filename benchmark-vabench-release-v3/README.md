# Behavioral Verilog-A v3

This directory is a clean, RTL-Forge-style packaging of 300 Verilog-A
DUT/support/testbench/e2e tasks.

Top-level indexes:

- `TASKS.json`: canonical task ids, titles, forms, directories, and target
  Verilog-A artifacts for all tasks.
- `CHECKS.yaml`: canonical checker configuration for all tasks, replacing
  per-task `test_harness/checks.yaml` files.

Partitions:

- `001`-`049`: migrated v1 DUT tasks.
- `050`-`079`: testbench utility / Verilog-A helper module tasks.
- `080`-`089`: additional migrated DUT/support modules from v1.
- `090`-`111`: additional useful Verilog-A module tasks promoted into v3.
- `112`-`300`: imported and repaired DUT/module tasks, including the obsolete
  v2 five-task slice absorbed as normal v3 tasks.

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
