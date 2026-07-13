# Reset Release Sequencer

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `reset_release_sequencer.va`: `reset_release_sequencer`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_INITIALIZE_THE_INTERNAL_STAGE_COUNT_AND`: Initialize the internal stage count and all observables to zero. On each rising clock crossing, clear the stage count when `rst` is high, `supply_ok <= vth`, or `bias_ok <= vth`. Otherwise increment the stage count by one until it reaches `final_stage`.
- `P_AFTER_UPDATING_THE_STAGE_COUNT_DRIVE`: After updating the stage count, drive `stage1 = vhi` when `stage_count >= 1`, `stage2 = vhi` when `stage_count >= 2`, and `ready = vhi` when `stage_count >= final_stage`; otherwise drive each of those observables to `0 V`. Drive `progress = vhi * clip01(stage_count / final_stage)`. Hold the last observable values between rising clock crossings.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `reset_release_sequencer.va`.
Do not add or omit artifacts.
