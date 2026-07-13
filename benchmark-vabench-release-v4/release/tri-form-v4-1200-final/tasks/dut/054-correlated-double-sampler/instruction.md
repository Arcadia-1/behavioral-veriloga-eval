# Correlated Double Sampler

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `correlated_double_sampler.va`: `correlated_double_sampler`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_SAMPLE`: A rising phi_reset crossing captures vin as the reset level, returns vout to vcm, and clears valid.
- `P_SIGNAL_CORRECTION`: A rising phi_signal crossing publishes vcm plus gain times the current signal sample minus the most recently captured reset sample.
- `P_OUTPUT_CLAMP`: The corrected output is limited to the inclusive vlo-to-vhi range.
- `P_VALID_SEQUENCE`: valid is low before a completed signal sample and after every reset sample, then rises to vhi when a signal sample is published.
- `P_HOLD_BETWEEN_EVENTS`: vout and valid hold their last event-updated states between reset and signal sampling crossings.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `correlated_double_sampler.va`.
Do not add or omit artifacts.
