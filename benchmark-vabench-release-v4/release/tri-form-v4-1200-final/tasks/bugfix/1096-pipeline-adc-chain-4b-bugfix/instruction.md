# Pipeline ADC Chain 4b Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `pipeline_adc_chain_4b.va`: `pipeline_adc_chain_4b`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_CLOCKED_SAMPLE_HOLD`: On each rising CLK crossing, the converter samples VIN and updates all stage residues and bits; outputs hold between conversions.
- `P_STAGE1_DECISION`: Stage 1 clips VIN to vrefn through vrefp, selects the correct quarter-scale bin, and exposes the two-bit coarse decision on S1B1/S1B0.
- `P_STAGE1_RESIDUE`: RES1 is four times the clipped sampled-input error from the selected stage-1 bin center, clipped to the conversion range.
- `P_STAGE2_DECISION`: Stage 2 applies the same quarter-scale two-bit decision to RES1 and exposes it on S2B1/S2B0.
- `P_STAGE2_RESIDUE`: RES2 is four times the stage-2 input error from its selected bin center, clipped to the conversion range.
- `P_FINAL_CODE_CONCATENATION`: DOUT3/DOUT2 equal the stage-1 bits and DOUT1/DOUT0 equal the stage-2 bits, using VDD for high and VSS for low.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `pipeline_adc_chain_4b.va`.
Every supplied `.va` file is editable; do not add or omit files.
