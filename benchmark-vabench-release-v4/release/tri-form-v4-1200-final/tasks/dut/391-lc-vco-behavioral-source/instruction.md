# LC VCO Behavioral Source

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `lc_vco_behavioral_source.va`: `lc_vco_behavioral_source`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_DISABLE_CENTER`: Reset or disable centers both oscillator outputs at vcm and clears metrics and valid.
- `P_CONTROL_FREQUENCY_MAP`: Enabled edge periods follow the linear clamped vctrl mapping from fmin to fmax without retiming an already pending edge.
- `P_COMPLEMENTARY_AMPLITUDE`: Enabled oscillator outputs are complementary around vcm with the declared amplitude.
- `P_METRIC_REPORTING`: freq_metric reports clamped vctrl and amp_metric reports amplitude while enabled.
- `P_VALID_AFTER_TWO_CYCLES`: valid remains low until two complete oscillator cycles have elapsed after enable.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `lc_vco_behavioral_source.va`.
Do not add or omit artifacts.
