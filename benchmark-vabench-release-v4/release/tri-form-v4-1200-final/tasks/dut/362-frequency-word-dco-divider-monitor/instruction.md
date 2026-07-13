# Frequency-word DCO with Divider Monitor

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `frequency_word_dco.va`: `frequency_word_dco`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_DISABLE_STOP`: Reset or disabled operation stops and clears both clocks, the divider counter, and the frequency metric.
- `P_FREQUENCY_WORD_MAPPING`: The six-bit frequency word maps to min(f_max, f_min plus f_step times code), with the public normalized metric matching that target.
- `P_DIVIDER_MONITOR`: div_clk toggles once per divide_ratio rising DCO edges and its counter restarts after reset or disable.
- `P_RESTART_MONOTONICITY`: Enable restarts both clocks low with the first DCO rise one half-period later, and larger frequency words produce nondecreasing edge counts.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `frequency_word_dco.va`.
Do not add or omit artifacts.
