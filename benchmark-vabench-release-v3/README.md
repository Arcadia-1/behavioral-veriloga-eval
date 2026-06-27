# Behavioral Verilog-A v3

This directory is a clean, RTL-Forge-style packaging of 287 Verilog-A
DUT/support/testbench/e2e tasks.

Partitions:

- `001`-`049`: migrated v1 DUT tasks.
- `050`-`079`: testbench utility / Verilog-A helper module tasks.
- `080`-`089`: additional migrated DUT/support modules from v1.
- `090`-`111`: additional useful Verilog-A module tasks promoted into v3.
- `112`-`282`: certified source-import DUT tasks.
- `283`-`287`: explicit absorption of the obsolete v2 five-task slice.

Each task is self-contained under `tasks/NNN-name/`:

- `instruction.md`: the problem statement the agent sees.
- `starter/`: files the agent edits.
- `test_visible/`: public smoke tests the agent may run.
- `test_hidden/`: hidden testbenches for grading.
- `test_harness/`: checker configuration and evaluation bridge files.
- `solution/`: golden reference implementation.
- `negative_variants/`: intentionally wrong implementations used to audit checker strength.
- `task.toml`: tooling index, not part of the agent prompt.

The agent-facing surface is intentionally small: `instruction.md`, `starter/`,
and `test_visible/`. Hidden tests, checker configs, golden solutions, and
negative variants are evaluator-side material.

Use [REVIEW_SOP.md](REVIEW_SOP.md) for manual admission review before counting a
task as independent benchmark coverage.

Task names describe the circuit/helper being built instead of preserving legacy migration ids. Private submission records, image tags, model ids, and other orchestration state remain outside this public benchmark tree.
