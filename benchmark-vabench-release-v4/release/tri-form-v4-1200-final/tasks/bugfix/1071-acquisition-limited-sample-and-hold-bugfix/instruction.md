# Acquisition Limited Sample And Hold Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `acquisition_limited_sample_hold.va`: `acquisition_limited_sample_hold`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET`: While rst is above vth, vout returns to vinit and metric is low.
- `P_ACQUISITION_ENABLE`: When sample is above vth and reset is inactive, metric is high and vout is allowed to acquire vin.
- `P_FINITE_ACQUISITION`: At each tick during acquisition, vout advances by alpha times the remaining difference from the current vin rather than jumping instantaneously.
- `P_ACQUISITION_CONVERGENCE`: For a constant vin and repeated acquisition updates, vout moves monotonically toward vin without overshoot for the declared alpha range.
- `P_HOLD`: A falling sample crossing freezes the last acquired value; vout holds it and metric remains low until acquisition resumes or reset is asserted.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `acquisition_limited_sample_hold.va`.
Every supplied `.va` file is editable; do not add or omit files.
