# Power and Reset Sequencer Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `power_reset_seq_top.va`: `power_reset_seq_top`
- `por_detector.va`: `por_detector`
- `reset_synchronizer.va`: `reset_synchronizer`
- `enable_sequencer.va`: `enable_sequencer`
- `ready_flag.va`: `ready_flag`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_PWR_ASYNC_CLEAR`: External reset or a brownout clears por_n, core reset release, enables, and ready without waiting for sequence completion.
- `P_PWR_POR_DEBOUNCE`: por_n asserts only after two consecutive good-power rising clock edges.
- `P_PWR_SEQUENCE_ORDER`: With power good and enable requested, rst_n_core, en_ana, and en_dig release on successive rising clock edges.
- `P_PWR_READY_DELAY`: ready asserts one rising clock after both enables are high.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `power_reset_seq_top.va`, `por_detector.va`, `reset_synchronizer.va`, `enable_sequencer.va`, `ready_flag.va`.
Every supplied `.va` file is editable; do not add or omit files.
