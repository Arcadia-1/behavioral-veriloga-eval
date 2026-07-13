# Duty-cycle Corrector Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `dcc_top.va`: `dcc_top`
- `duty_meter.va`: `duty_meter`
- `trim_controller.va`: `trim_controller`
- `delay_pair.va`: `delay_pair`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_DISABLE_CLEAR`: Reset or low enable clears trim, duty metric, lock, and output clock.
- `P_DUTY_MEASUREMENT`: The metric reports high-time fraction over each complete input-clock cycle.
- `P_TRIM_DIRECTION`: The trim code moves up below the target window and down above it, with rail saturation.
- `P_EDGE_DELAY`: Rising edges pass without intentional delay while falling edges receive the latched trim-code delay.
- `P_LOCK_QUALIFICATION`: Lock asserts after three consecutive measured cycles inside the target window.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `dcc_top.va`, `duty_meter.va`, `trim_controller.va`, `delay_pair.va`.
Every supplied `.va` file is editable; do not add or omit files.
