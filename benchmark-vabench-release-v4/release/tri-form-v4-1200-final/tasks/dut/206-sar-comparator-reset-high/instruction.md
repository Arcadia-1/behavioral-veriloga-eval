# SAR Comparator Reset High

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `sar_comparator_reset_high.va`: `sar_comparator_reset_high`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_INITIALIZE_BOTH_DECISION_OUTPUTS_HIGH_WHENEVER`: Initialize both decision outputs high. Whenever `cmpck` falls through `vdd/2`, reset both outputs high. Whenever `cmpck` rises through `vdd/2`, latch a differential decision: `dcmpp` high for `vinp > vinn`, `dcmpn` high for `vinp < vinn`, and both outputs low for equal inputs. Hold the latched or reset state until the next clock event.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `sar_comparator_reset_high.va`.
Do not add or omit artifacts.
