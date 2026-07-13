# Quadrature Oscillator Phase-error Monitor

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `quadrature_oscillator_phase_error_monitor.va`: `quadrature_oscillator_phase_error_monitor`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear phase metric, status, and `valid`.
- `P_TRACK_RISING_THRESHOLD_CROSSINGS_OF_CLK`: Track rising threshold crossings of `clk_i` and `clk_q`.
- `P_ESTIMATE_A_VOLTAGE_DOMAIN_PHASE_ERROR`: Estimate a voltage-domain phase-error metric from the relative event order and interval proxy.
- `P_ASSERT_QUADRATURE_OK_WHEN_THE_MEASURED`: Assert `quadrature_ok` when the measured phase proxy stays within `phase_tol` for two cycles.
- `P_ASSERT_VALID_AFTER_BOTH_I_AND`: Assert `valid` after both I and Q edges have been observed.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `quadrature_oscillator_phase_error_monitor.va`.
Do not add or omit artifacts.
