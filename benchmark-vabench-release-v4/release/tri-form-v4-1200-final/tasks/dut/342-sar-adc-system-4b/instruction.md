# 4-bit SAR ADC System

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `sar_adc_top.va`: `sar_adc_top`
- `sample_hold.va`: `sample_hold`
- `sar_comparator.va`: `sar_comparator`
- `sar_controller.va`: `sar_controller`
- `binary_weighted_cdac.va`: `binary_weighted_cdac`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_SAR_RESET_CLEAR`: Reset clears conversion state, code, done, sample_dbg, and dac_dbg.
- `P_SAR_SAMPLE_HOLD`: The first rising clock edge after start captures vin and sample_dbg holds that value through conversion.
- `P_SAR_FINAL_CODE`: Four MSB-first trials quantize the held sample to the clamped unsigned 4-bit SAR code.
- `P_SAR_DAC_TRIAL`: dac_dbg exposes vref times the active trial code divided by 16 and settles to the final-code DAC level.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `sar_adc_top.va`, `sample_hold.va`, `sar_comparator.va`, `sar_controller.va`, `binary_weighted_cdac.va`.
Do not add or omit artifacts.
