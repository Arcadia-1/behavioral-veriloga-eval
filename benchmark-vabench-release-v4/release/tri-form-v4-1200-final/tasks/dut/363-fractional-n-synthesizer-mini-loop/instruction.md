# Fractional-N Synthesizer Mini Loop

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `fracn_synth_top.va`: `fracn_synth_top`
- `accumulator.va`: `accumulator`
- `multi_modulus_divider.va`: `multi_modulus_divider`
- `ratio_monitor.va`: `ratio_monitor`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_DISABLE_CLEAR`: Reset or disabled operation clears accumulator/divider state and all public outputs.
- `P_FRACTIONAL_SELECTION`: The fraction code drives deterministic n_int versus n_int+1 selection through accumulator carry events.
- `P_DCO_DERIVED_DIVIDER`: div_clk transitions are derived only from counted rising dco_clk edges using the selected modulus.
- `P_RATIO_WINDOW`: At each full window, avg_ratio_metric reports n_int plus the observed fraction of larger-modulus selections and valid pulses.
- `P_FRACTION_MONOTONICITY`: Larger fraction commands produce nondecreasing average selected divide-ratio metrics over equal windows.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `fracn_synth_top.va`, `accumulator.va`, `multi_modulus_divider.va`, `ratio_monitor.va`.
Do not add or omit artifacts.
