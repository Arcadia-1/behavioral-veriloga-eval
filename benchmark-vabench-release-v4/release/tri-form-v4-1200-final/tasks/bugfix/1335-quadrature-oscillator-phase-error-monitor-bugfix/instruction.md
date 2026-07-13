# Quadrature Oscillator Phase-error Monitor Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `quadrature_oscillator_phase_error_monitor.va`: `quadrature_oscillator_phase_error_monitor`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear phase metric, status, and `valid`.
- `P_TRACK_RISING_THRESHOLD_CROSSINGS_OF_CLK`: Track rising threshold crossings of `clk_i` and `clk_q`.
- `P_ESTIMATE_A_VOLTAGE_DOMAIN_PHASE_ERROR`: Estimate a voltage-domain phase-error metric from the relative event order and interval proxy.
- `P_ASSERT_QUADRATURE_OK_WHEN_THE_MEASURED`: Assert `quadrature_ok` when the measured phase proxy stays within `phase_tol` for two cycles.
- `P_ASSERT_VALID_AFTER_BOTH_I_AND`: Assert `valid` after both I and Q edges have been observed.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `quadrature_oscillator_phase_error_monitor.va`.
Every supplied `.va` file is editable; do not add or omit files.
