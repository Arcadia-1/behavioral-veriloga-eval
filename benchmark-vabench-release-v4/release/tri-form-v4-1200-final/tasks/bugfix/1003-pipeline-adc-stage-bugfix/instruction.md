# Pipeline ADC Stage Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `pipeline_stage.va`: `pipeline_stage`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_TWO_PHASE_SAMPLING`: VIN is sampled on a rising PHI1 edge and converted on a rising PHI2 edge.
- `P_SUBADC_REGIONS`: Upper, middle, and lower sampled-input regions produce decision codes 10, 01, and 00 respectively.
- `P_RESIDUE_MAPPING`: The residue is gain-two with the specified half-reference subtraction, no offset, or addition for the three regions.
- `P_RESIDUE_CLAMP`: VRES remains within the VSS-to-VDD supply range.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `pipeline_stage.va`.
Every supplied `.va` file is editable; do not add or omit files.
