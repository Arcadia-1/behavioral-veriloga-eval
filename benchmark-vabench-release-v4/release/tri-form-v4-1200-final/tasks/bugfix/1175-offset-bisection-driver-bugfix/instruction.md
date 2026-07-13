# Offset Bisection Driver Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `offset_bisection_driver.va`: `offset_bisection_driver`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_BISECTION_INITIAL_STATE`: The differential residue initializes to zero, the step initializes to `step_initial`, and the previous decision polarity initializes to the low-decision direction.
- `P_FALLING_CLOCK_DECISION_UPDATE`: On each falling `clk` crossing, sample `vout` and update the residue using the specified comparator polarity.
- `P_SIGN_CHANGE_STEP_HALVING`: The bisection step halves when the sampled decision polarity changes.
- `P_VCM_CENTERED_DIFFERENTIAL_DRIVE`: `vinp` and `vinn` remain centered around `vcm` with half of the differential residue on each side.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `offset_bisection_driver.va`.
Every supplied `.va` file is editable; do not add or omit files.
