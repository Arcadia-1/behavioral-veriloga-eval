# Polyphase I/Q Balance Monitor Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `polyphase_iq_balance_monitor_top.va`: `polyphase_iq_balance_monitor_top`
- `iq_normalizer.va`: `iq_normalizer`
- `balance_metric_core.va`: `balance_metric_core`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive outputs to `vcm` and clear metrics.
- `P_ON_EACH_ENABLED_RISING_CLK_EDGE`: On each enabled rising `clk` edge, sample I and Q input deviations around `vcm`.
- `P_DRIVE_CORRECTED_I_Q_OUTPUTS_WITH`: Drive corrected I/Q outputs with bounded amplitude normalization.
- `P_EXPOSE_AMPLITUDE_AND_PHASE_ERROR_PROXIES`: Expose amplitude and phase-error proxies as separate voltage-domain metrics.
- `P_ASSERT_BALANCED_ONLY_WHEN_BOTH_METRICS`: Assert `balanced` only when both metrics remain below their thresholds for two updates.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `polyphase_iq_balance_monitor_top.va`, `iq_normalizer.va`, `balance_metric_core.va`.
Every supplied `.va` file is editable; do not add or omit files.
