# Ideal Clkmux 8channel

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `ideal_clkmux_8channel.va`: `ideal_clkmux_8channel`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_MODULO8_COUNTER`: The internal selector starts at zero and increments modulo eight on each rising `clk` crossing through 0.5 V.
- `P_INCREMENT_BEFORE_SELECTION`: The first qualifying clock event selects the incremented counter state rather than the reset state.
- `P_ANALOG_CHANNEL_MUX`: `out` follows the input channel selected by the current counter value.
- `P_COUNTER_MONITOR_LEVEL`: `count_x` reports the current selector count with the specified voltage scaling.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `ideal_clkmux_8channel.va`.
Do not add or omit artifacts.
