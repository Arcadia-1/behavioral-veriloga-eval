# LDO Load Step Recovery Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `ldo_load_step_recovery_flow.va`: `ldo_load_step_recovery_flow`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_REGULATION_STATE`: Active-high reset initializes out and target to 0.60 V, load_mon to 0.10 V, ctrl_mon to 0.50 V, metric to 0.9 V, and clears recovery progress.
- `P_BOUNDED_LOAD_AND_TARGET`: Each non-reset rising clk edge clips vin to 0 V through 0.9 V on load_mon and uses the public load-dependent target 0.61 V minus 0.025 times load.
- `P_CONTROL_MONITOR`: Ctrl_mon represents the public load and regulation-error control expression and remains clamped to 0.05 V through 0.85 V.
- `P_HEAVY_LOAD_DROOP`: A sampled load increase greater than 0.20 V causes the public 0.13 V transient droop before first-order recovery and restarts recovery qualification.
- `P_LIGHT_LOAD_KICK`: A sampled load decrease greater than 0.20 V causes the public 0.05 V light-load recovery kick before first-order recovery and restarts qualification.
- `P_RECOVERY_AND_SETTLING`: Every non-reset update applies the public 0.30 first-order recovery, clamps out to 0.20 V through 0.75 V, and sets metric high only after at least five updates with target error below 0.045 V.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `ldo_load_step_recovery_flow.va`.
Every supplied `.va` file is editable; do not add or omit files.
