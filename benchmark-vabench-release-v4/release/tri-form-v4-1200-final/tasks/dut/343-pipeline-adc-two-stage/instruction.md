# Two-stage Pipeline ADC Mini Chain

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `pipeline_adc_top.va`: `pipeline_adc_top`
- `stage1_quantizer.va`: `stage1_quantizer`
- `residue_amp.va`: `residue_amp`
- `stage2_quantizer.va`: `stage2_quantizer`
- `code_aligner.va`: `code_aligner`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_PIPE_RESET_CLEAR`: Reset clears both stages, output code, valid_o, and residue_dbg.
- `P_PIPE_RESIDUE`: A valid input sample produces the four-times normalized residue for its coarse quarter range.
- `P_PIPE_ALIGNED_CODE`: The delayed coarse and fine decisions align into the clamped 4-bit conversion code.
- `P_PIPE_VALID_LATENCY`: valid_o accompanies each completed pipeline result and no reset result is marked valid.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `pipeline_adc_top.va`, `stage1_quantizer.va`, `residue_amp.va`, `stage2_quantizer.va`, `code_aligner.va`.
Do not add or omit artifacts.
