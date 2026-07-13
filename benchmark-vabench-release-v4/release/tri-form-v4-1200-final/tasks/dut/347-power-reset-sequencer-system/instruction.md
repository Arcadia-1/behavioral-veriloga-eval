# Power and Reset Sequencer

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `power_reset_seq_top.va`: `power_reset_seq_top`
- `por_detector.va`: `por_detector`
- `reset_synchronizer.va`: `reset_synchronizer`
- `enable_sequencer.va`: `enable_sequencer`
- `ready_flag.va`: `ready_flag`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_PWR_ASYNC_CLEAR`: External reset or a brownout clears por_n, core reset release, enables, and ready without waiting for sequence completion.
- `P_PWR_POR_DEBOUNCE`: por_n asserts only after two consecutive good-power rising clock edges.
- `P_PWR_SEQUENCE_ORDER`: With power good and enable requested, rst_n_core, en_ana, and en_dig release on successive rising clock edges.
- `P_PWR_READY_DELAY`: ready asserts one rising clock after both enables are high.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `power_reset_seq_top.va`, `por_detector.va`, `reset_synchronizer.va`, `enable_sequencer.va`, `ready_flag.va`.
Do not add or omit artifacts.
