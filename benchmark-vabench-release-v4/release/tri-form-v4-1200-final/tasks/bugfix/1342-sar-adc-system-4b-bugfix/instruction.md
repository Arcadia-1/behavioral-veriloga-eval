# 4-bit SAR ADC System Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `sar_adc_top.va`: `sar_adc_top`
- `sample_hold.va`: `sample_hold`
- `sar_comparator.va`: `sar_comparator`
- `sar_controller.va`: `sar_controller`
- `binary_weighted_cdac.va`: `binary_weighted_cdac`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_SAR_RESET_CLEAR`: Reset clears conversion state, code, done, sample_dbg, and dac_dbg.
- `P_SAR_SAMPLE_HOLD`: The first rising clock edge after start captures vin and sample_dbg holds that value through conversion.
- `P_SAR_FINAL_CODE`: Four MSB-first trials quantize the held sample to the clamped unsigned 4-bit SAR code.
- `P_SAR_DAC_TRIAL`: dac_dbg exposes vref times the active trial code divided by 16 and settles to the final-code DAC level.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `sar_adc_top.va`, `sample_hold.va`, `sar_comparator.va`, `sar_controller.va`, `binary_weighted_cdac.va`.
Every supplied `.va` file is editable; do not add or omit files.
