# Fixed-frequency Oscillator Source Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `fixed_frequency_oscillator_source.va`: `fixed_frequency_oscillator_source`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive `osc_out`, `period_metric`, and `valid` low.
- `P_WHEN_ENABLED_GENERATE_A_PERIODIC_VOLTAGE`: When enabled, generate a periodic voltage-domain clock that toggles between `vss` and `vdd` with the configured period.
- `P_PERIOD_METRIC_MUST_EXPOSE_A_STABLE`: `period_metric` must expose a stable voltage-coded representation of the configured period after the first complete cycle.
- `P_ASSERT_VALID_AFTER_THE_FIRST_COMPLETE`: Assert `valid` after the first complete oscillator cycle following enable.
- `P_RESET_OR_DISABLE_MUST_RESTART_THE`: Reset or disable must restart the oscillator phase deterministically.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `fixed_frequency_oscillator_source.va`.
Every supplied `.va` file is editable; do not add or omit files.
