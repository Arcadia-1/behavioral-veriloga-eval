# Loop Filter Abstraction Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `loop_filter_abstraction.va`: `loop_filter_abstraction`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_STATE`: Active reset restores the proportional state to 0.45 V, the step to 0.20 V, the integral residual and accepted-update count to zero, and metric to 0 V.
- `P_DEADBAND_HOLD`: At a rising clk crossing, an error vin - 0.45 V whose magnitude does not exceed deadband produces no proportional, integral, step, or count update.
- `P_SIGNED_UPDATE`: Each accepted positive error increases the proportional state by the current step and each accepted negative error decreases it, while the integral residual accumulates 0.04 times the sampled error.
- `P_STEP_HALVING`: The proportional step halves after every accepted update, producing successively smaller proportional corrections for equal-sign errors.
- `P_LOCK_COUNT_METRIC`: Metric remains low for fewer than four accepted updates and is 0.9 V once the accepted-update count reaches four; reset clears it.
- `P_PROPORTIONAL_CLAMP`: The proportional state is clamped to 0.05 V through 0.85 V before the accumulated integral residual is added to form out.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `loop_filter_abstraction.va`.
Every supplied `.va` file is editable; do not add or omit files.
