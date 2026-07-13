# Sample Hold Droop Front End

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `sample_hold_droop_ref.va`: `sample_hold_droop_ref`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_APERTURE_CAPTURE`: Each rising clk crossing schedules capture of vin after taperture rather than sampling at an unrelated time.
- `P_SUPPLY_CLAMPED_SAMPLE`: At aperture capture, the held output updates to the sampled vin clamped between the instantaneous vss and vdd rails.
- `P_COARSE_DECISION`: At each capture, coarse is high when the sampled value exceeds vth and low otherwise, then holds until the next capture.
- `P_VALID_PULSE`: Valid asserts at the aperture sample and deasserts after valid_width.
- `P_LOW_PHASE_DROOP`: While clk is low, vout applies bounded droop updates governed by tau and dt instead of remaining ideal or changing discontinuously.
- `P_NO_TRACK_THROUGH`: Between aperture captures, vout does not transparently track changes on vin; only the specified droop behavior is permitted.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `sample_hold_droop_ref.va`.
Do not add or omit artifacts.
