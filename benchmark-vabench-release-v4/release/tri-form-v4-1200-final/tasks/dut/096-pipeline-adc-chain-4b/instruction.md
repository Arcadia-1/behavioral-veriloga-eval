# Pipeline ADC Chain 4b

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `pipeline_adc_chain_4b.va`: `pipeline_adc_chain_4b`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_CLOCKED_SAMPLE_HOLD`: On each rising CLK crossing, the converter samples VIN and updates all stage residues and bits; outputs hold between conversions.
- `P_STAGE1_DECISION`: Stage 1 clips VIN to vrefn through vrefp, selects the correct quarter-scale bin, and exposes the two-bit coarse decision on S1B1/S1B0.
- `P_STAGE1_RESIDUE`: RES1 is four times the clipped sampled-input error from the selected stage-1 bin center, clipped to the conversion range.
- `P_STAGE2_DECISION`: Stage 2 applies the same quarter-scale two-bit decision to RES1 and exposes it on S2B1/S2B0.
- `P_STAGE2_RESIDUE`: RES2 is four times the stage-2 input error from its selected bin center, clipped to the conversion range.
- `P_FINAL_CODE_CONCATENATION`: DOUT3/DOUT2 equal the stage-1 bits and DOUT1/DOUT0 equal the stage-2 bits, using VDD for high and VSS for low.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `pipeline_adc_chain_4b.va`.
Do not add or omit artifacts.
