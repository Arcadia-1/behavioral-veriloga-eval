# Sigma-delta Modulator Mini Loop

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `sigma_delta_top.va`: `sigma_delta_top`
- `integrator_state.va`: `integrator_state`
- `sd_comparator.va`: `sd_comparator`
- `feedback_dac.va`: `feedback_dac`
- `decimator_lite.va`: `decimator_lite`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_CLEAR`: Reset clears the loop state, output bit, and decimator result.
- `P_FEEDBACK_STATE_UPDATE`: Each rising clock edge updates the bounded integrator from VIN and the previous feedback bit.
- `P_COMPARATOR_DECISION`: The output bit reflects the updated state relative to VCM.
- `P_DECIMATOR_WINDOW`: The four-bit result reports the saturated high-bit count for each complete 16-sample window.
- `P_STATE_BOUNDED`: The public state metric remains within the configured state limit.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `sigma_delta_top.va`, `integrator_state.va`, `sd_comparator.va`, `feedback_dac.va`, `decimator_lite.va`.
Do not add or omit artifacts.
