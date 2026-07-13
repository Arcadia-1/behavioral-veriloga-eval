# Sample Hold Droop Front End Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `sample_hold_droop_ref.va`: `sample_hold_droop_ref`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_APERTURE_CAPTURE`: Each rising clk crossing schedules capture of vin after taperture rather than sampling at an unrelated time.
- `P_SUPPLY_CLAMPED_SAMPLE`: At aperture capture, the held output updates to the sampled vin clamped between the instantaneous vss and vdd rails.
- `P_COARSE_DECISION`: At each capture, coarse is high when the sampled value exceeds vth and low otherwise, then holds until the next capture.
- `P_VALID_PULSE`: Valid asserts at the aperture sample and deasserts after valid_width.
- `P_LOW_PHASE_DROOP`: While clk is low, vout applies bounded droop updates governed by tau and dt instead of remaining ideal or changing discontinuously.
- `P_NO_TRACK_THROUGH`: Between aperture captures, vout does not transparently track changes on vin; only the specified droop behavior is permitted.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `sample_hold_droop_ref.va`.
Every supplied `.va` file is editable; do not add or omit files.
