# Reset Release Sequencer Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `reset_release_sequencer.va`: `reset_release_sequencer`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_INITIALIZE_THE_INTERNAL_STAGE_COUNT_AND`: Initialize the internal stage count and all observables to zero. On each rising clock crossing, clear the stage count when `rst` is high, `supply_ok <= vth`, or `bias_ok <= vth`. Otherwise increment the stage count by one until it reaches `final_stage`.
- `P_AFTER_UPDATING_THE_STAGE_COUNT_DRIVE`: After updating the stage count, drive `stage1 = vhi` when `stage_count >= 1`, `stage2 = vhi` when `stage_count >= 2`, and `ready = vhi` when `stage_count >= final_stage`; otherwise drive each of those observables to `0 V`. Drive `progress = vhi * clip01(stage_count / final_stage)`. Hold the last observable values between rising clock crossings.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `reset_release_sequencer.va`.
Every supplied `.va` file is editable; do not add or omit files.
