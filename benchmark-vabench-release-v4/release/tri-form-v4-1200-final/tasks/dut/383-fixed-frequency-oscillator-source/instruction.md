# Fixed-frequency Oscillator Source

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `fixed_frequency_oscillator_source.va`: `fixed_frequency_oscillator_source`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive `osc_out`, `period_metric`, and `valid` low.
- `P_WHEN_ENABLED_GENERATE_A_PERIODIC_VOLTAGE`: When enabled, generate a periodic voltage-domain clock that toggles between `vss` and `vdd` with the configured period.
- `P_PERIOD_METRIC_MUST_EXPOSE_A_STABLE`: `period_metric` must expose a stable voltage-coded representation of the configured period after the first complete cycle.
- `P_ASSERT_VALID_AFTER_THE_FIRST_COMPLETE`: Assert `valid` after the first complete oscillator cycle following enable.
- `P_RESET_OR_DISABLE_MUST_RESTART_THE`: Reset or disable must restart the oscillator phase deterministically.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `fixed_frequency_oscillator_source.va`.
Do not add or omit artifacts.
