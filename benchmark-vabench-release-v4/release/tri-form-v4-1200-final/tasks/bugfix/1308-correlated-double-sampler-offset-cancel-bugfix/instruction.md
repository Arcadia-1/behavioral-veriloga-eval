# Correlated Double Sampler Offset-cancel Macro Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `correlated_double_sampler_top.va`: `correlated_double_sampler_top`
- `reset_sample_latch.va`: `reset_sample_latch`
- `signal_sample_latch.va`: `signal_sample_latch`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_CLEAR_RESET_SAMPLE_SIGNAL`: On reset, clear reset-sample, signal-sample, output, debug metric, and `valid`.
- `P_ON_A_RISING_CLK_EDGE_WITH`: On a rising `clk` edge with `sample_reset` high, capture `vin` as the reset/reference sample.
- `P_ON_A_LATER_RISING_CLK_EDGE`: On a later rising `clk` edge with `sample_signal` high, capture `vin` as the signal sample.
- `P_DRIVE_VOUT_AS_VCM_PLUS_THE`: Drive `vout` as `vcm` plus the signal-minus-reset difference scaled by `cds_gain`.
- `P_EXPOSE_THE_RESET_SAMPLE_ON_OFFSET`: Expose the reset sample on `offset_dbg` and assert `valid` only after a complete reset/signal pair.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `correlated_double_sampler_top.va`, `reset_sample_latch.va`, `signal_sample_latch.va`.
Every supplied `.va` file is editable; do not add or omit files.
