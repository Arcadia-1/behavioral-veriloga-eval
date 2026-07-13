# Fractional-N Synthesizer Mini Loop Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `fracn_synth_top.va`: `fracn_synth_top`
- `accumulator.va`: `accumulator`
- `multi_modulus_divider.va`: `multi_modulus_divider`
- `ratio_monitor.va`: `ratio_monitor`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_DISABLE_CLEAR`: Reset or disabled operation clears accumulator/divider state and all public outputs.
- `P_FRACTIONAL_SELECTION`: The fraction code drives deterministic n_int versus n_int+1 selection through accumulator carry events.
- `P_DCO_DERIVED_DIVIDER`: div_clk transitions are derived only from counted rising dco_clk edges using the selected modulus.
- `P_RATIO_WINDOW`: At each full window, avg_ratio_metric reports n_int plus the observed fraction of larger-modulus selections and valid pulses.
- `P_FRACTION_MONOTONICITY`: Larger fraction commands produce nondecreasing average selected divide-ratio metrics over equal windows.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `fracn_synth_top.va`, `accumulator.va`, `multi_modulus_divider.va`, `ratio_monitor.va`.
Every supplied `.va` file is editable; do not add or omit files.
