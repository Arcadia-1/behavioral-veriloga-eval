# Polyphase I/Q Balance Monitor

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `polyphase_iq_balance_monitor_top.va`: `polyphase_iq_balance_monitor_top`
- `iq_normalizer.va`: `iq_normalizer`
- `balance_metric_core.va`: `balance_metric_core`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive outputs to `vcm` and clear metrics.
- `P_ON_EACH_ENABLED_RISING_CLK_EDGE`: On each enabled rising `clk` edge, sample I and Q input deviations around `vcm`.
- `P_DRIVE_CORRECTED_I_Q_OUTPUTS_WITH`: Drive corrected I/Q outputs with bounded amplitude normalization.
- `P_EXPOSE_AMPLITUDE_AND_PHASE_ERROR_PROXIES`: Expose amplitude and phase-error proxies as separate voltage-domain metrics.
- `P_ASSERT_BALANCED_ONLY_WHEN_BOTH_METRICS`: Assert `balanced` only when both metrics remain below their thresholds for two updates.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `polyphase_iq_balance_monitor_top.va`, `iq_normalizer.va`, `balance_metric_core.va`.
Do not add or omit artifacts.
