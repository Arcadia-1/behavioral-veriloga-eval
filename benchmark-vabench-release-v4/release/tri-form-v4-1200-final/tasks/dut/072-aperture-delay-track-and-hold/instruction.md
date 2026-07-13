# Aperture Delay Track And Hold

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `sample_hold_aperture_ref.va`: `sample_hold_aperture_ref`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_INITIAL_VALUE`: At initialization, the held output is established from the initial observed vin value.
- `P_APERTURE_ARM`: Each rising crossing of clk through vth arms exactly one sample for the corresponding delayed aperture instant.
- `P_DELAYED_CAPTURE`: At taperture after the rising clk crossing, vout captures the vin value present at that delayed instant rather than at the clock edge.
- `P_HOLD`: Between delayed aperture instants, vout retains the most recently captured value and does not track vin.
- `P_RAIL_OBSERVABILITY`: VDD and VSS are public supply-observation ports for harness compatibility only; they do not clamp, scale, or shift the captured vin value.
- `P_OUTPUT_SMOOTHING`: Changes in the held value appear on vout with finite transition smoothing set by tedge.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `sample_hold_aperture_ref.va`.
Do not add or omit artifacts.
