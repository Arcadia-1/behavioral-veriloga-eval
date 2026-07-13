# Aperture Delay Track And Hold Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `sample_hold_aperture_ref.va`: `sample_hold_aperture_ref`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_INITIAL_VALUE`: At initialization, the held output is established from the initial observed vin value.
- `P_APERTURE_ARM`: Each rising crossing of clk through vth arms exactly one sample for the corresponding delayed aperture instant.
- `P_DELAYED_CAPTURE`: At taperture after the rising clk crossing, vout captures the vin value present at that delayed instant rather than at the clock edge.
- `P_HOLD`: Between delayed aperture instants, vout retains the most recently captured value and does not track vin.
- `P_RAIL_OBSERVABILITY`: VDD and VSS are public supply-observation ports for harness compatibility only; they do not clamp, scale, or shift the captured vin value.
- `P_OUTPUT_SMOOTHING`: Changes in the held value appear on vout with finite transition smoothing set by tedge.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `sample_hold_aperture_ref.va`.
Every supplied `.va` file is editable; do not add or omit files.
