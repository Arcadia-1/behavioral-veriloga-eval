# Behavioral Verilog-A v3

This directory is a clean, RTL-Forge-style packaging of 79 Verilog-A DUT/support tasks.

Partitions:

- `001`-`049`: DUT repair/evaluation candidates.
- `050`-`079`: support-staging testbench utility / Verilog-A helper module candidates.

Each task is self-contained under `tasks/NNN-name/`:

- `instruction.md`: the problem statement the agent sees.
- `starter/`: files the agent edits.
- `test_visible/`: public smoke tests the agent may run.
- `test_hidden/`: hidden testbenches for grading.
- `test_harness/`: checker configuration and evaluation bridge files.
- `solution/`: golden reference implementation.
- `negative_variants/`: intentionally wrong implementations or staging negative plans used to audit checker strength.
- `task.toml`: tooling index, not part of the agent prompt.

Task names describe the circuit/helper being built instead of preserving legacy migration ids. Private submission records, image tags, model ids, and other orchestration state remain outside this public benchmark tree.
