# Supply Supervisor with Brownout POR Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `supply_supervisor_brownout_por.va`: `supply_supervisor_brownout_por`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_DISABLE_SAFE`: Reset or disable asserts brownout, holds POR low, clears pgood and both metrics.
- `P_UVLO_HYSTERESIS`: Supply below uvlo_fall enters brownout and supply must exceed uvlo_rise to leave it.
- `P_RELEASE_DELAY`: POR and pgood assert only after release_cycles consecutive good rising clock edges.
- `P_DIP_RESTART`: A supply dip below uvlo_fall immediately reasserts brownout and clears release progress.
- `P_STATE_METRICS`: Delay and state metrics report the saturated release count and four public supervisor states.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `supply_supervisor_brownout_por.va`.
Every supplied `.va` file is editable; do not add or omit files.
