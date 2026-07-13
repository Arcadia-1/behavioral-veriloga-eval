# Digitally Controlled Delay Cell

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `digitally_controlled_delay_cell.va`: `digitally_controlled_delay_cell`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_CLEAR`: Reset clears the loaded code state, delayed clock, delay metric, valid indication, and pending edges.
- `P_CODE_CAPTURE_METRIC`: A rising load edge captures the six-bit unsigned code and the delay metric reports the normalized captured code.
- `P_EDGE_DELAY_MAPPING`: Each input-clock edge appears at the output after delay_min plus delay_lsb times the code captured for that edge.
- `P_PULSE_INTEGRITY_VALID`: Rising and falling edges receive equal delay, preserving pulse width, and valid asserts after the first delayed rising edge.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `digitally_controlled_delay_cell.va`.
Do not add or omit artifacts.
