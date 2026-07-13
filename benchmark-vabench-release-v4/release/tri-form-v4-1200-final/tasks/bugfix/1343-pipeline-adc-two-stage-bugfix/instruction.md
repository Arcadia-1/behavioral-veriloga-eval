# Two-stage Pipeline ADC Mini Chain Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `pipeline_adc_top.va`: `pipeline_adc_top`
- `stage1_quantizer.va`: `stage1_quantizer`
- `residue_amp.va`: `residue_amp`
- `stage2_quantizer.va`: `stage2_quantizer`
- `code_aligner.va`: `code_aligner`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_PIPE_RESET_CLEAR`: Reset clears both stages, output code, valid_o, and residue_dbg.
- `P_PIPE_RESIDUE`: A valid input sample produces the four-times normalized residue for its coarse quarter range.
- `P_PIPE_ALIGNED_CODE`: The delayed coarse and fine decisions align into the clamped 4-bit conversion code.
- `P_PIPE_VALID_LATENCY`: valid_o accompanies each completed pipeline result and no reset result is marked valid.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `pipeline_adc_top.va`, `stage1_quantizer.va`, `residue_amp.va`, `stage2_quantizer.va`, `code_aligner.va`.
Every supplied `.va` file is editable; do not add or omit files.
