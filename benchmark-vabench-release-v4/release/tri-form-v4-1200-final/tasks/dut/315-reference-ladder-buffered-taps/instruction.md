# Reference Ladder with Buffered Taps

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `reference_ladder_buffered_taps.va`: `reference_ladder_buffered_taps`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive taps to `vss` and clear `monotonic_ok`.
- `P_WHEN_ENABLED_GENERATE_FOUR_EVENLY_SPACED`: When enabled, generate four evenly spaced buffered tap voltages between `vref_lo` and `vref_hi`.
- `P_CLAMP_REVERSED_OR_OUT_OF_RANGE`: Clamp reversed or out-of-range references into the public rail range before generating taps.
- `P_ASSERT_MONOTONIC_OK_ONLY_WHEN_THE`: Assert `monotonic_ok` only when the exposed tap sequence is nondecreasing.
- `P_SMOOTH_TAP_OUTPUT_TRANSITIONS_WITH_THE`: Smooth tap output transitions with the public transition parameter.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `reference_ladder_buffered_taps.va`.
Do not add or omit artifacts.
