# Configurable Polarity Edge Detector

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `configurable_polarity_edge_detector.va`: `configurable_polarity_edge_detector`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RISING_SELECTION`: When rise_en is above vth, each rising crossing of sig through vth produces one output pulse.
- `P_FALLING_SELECTION`: When rise_en is below vth, each falling crossing of sig through vth produces one output pulse.
- `P_OPPOSITE_EDGE_REJECTION`: An edge opposite to the polarity selected by rise_en does not produce a pulse.
- `P_BOUNDED_PULSE`: Each detected edge produces a bounded short pulse with nominal width about 2 ns rather than a latched high level.
- `P_OUTPUT_LEVELS`: pulse uses 0 V and vdd levels with finite transition smoothing set by tr.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `configurable_polarity_edge_detector.va`.
Do not add or omit artifacts.
