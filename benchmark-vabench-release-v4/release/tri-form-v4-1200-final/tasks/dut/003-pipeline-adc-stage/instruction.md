# Pipeline ADC Stage

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `pipeline_stage.va`: `pipeline_stage`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_TWO_PHASE_SAMPLING`: VIN is sampled on a rising PHI1 edge and converted on a rising PHI2 edge.
- `P_SUBADC_REGIONS`: Upper, middle, and lower sampled-input regions produce decision codes 10, 01, and 00 respectively.
- `P_RESIDUE_MAPPING`: The residue is gain-two with the specified half-reference subtraction, no offset, or addition for the three regions.
- `P_RESIDUE_CLAMP`: VRES remains within the VSS-to-VDD supply range.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `pipeline_stage.va`.
Do not add or omit artifacts.
