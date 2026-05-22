# vaBench Release Prompt Contract Manifest

Date: 2026-05-22

| Metric | Value |
| --- | ---: |
| status | `pass` |
| prompt version | `public-contract-v2` |
| prompts | 263 |

## Form Counts

| Form | Prompts |
| --- | ---: |
| `bugfix` | 53 |
| `dut` | 58 |
| `e2e` | 76 |
| `tb` | 76 |

## Change Summary

- Normalized all release prompts to explicit public benchmark contracts.
- Moved runner-only wrapper, ICL, and repair-feedback protocol out of public prompts.
- Recorded target artifact names from release_task/gold assets for prompt-version traceability.
- Old model-baseline results should be treated as historical and rerun before comparison.

## Claim Policy

- Public prompts are benchmark contracts: task contract only: form, target artifacts, interfaces, public observables, public behavior checks, and output contract.
- Runner wrappers remain outside the prompt body: model invocation protocol, output extraction markers, optional repair feedback, and optional ICL variants.
- EVAS rules remain shared runner guidance: shared voltage-domain and EVAS/Spectre compatibility guidance injected by runners, not benchmark prompt content.
- Baseline comparability: pre-public-contract-v2 and public-contract-v2 results are not directly comparable without rerun.

## Sample Rows

| Task | Form | Target Artifacts | Prompt SHA256 |
| --- | --- | --- | --- |
| `vbr1_l1_binary_weighted_voltage_dac:bugfix` | `bugfix` | `dut_fixed.va` | `aa43a793a850` |
| `vbr1_l1_binary_weighted_voltage_dac:dut` | `dut` | `simple_binary_voltage_dac_4b.va` | `42a6bf7afb2c` |
| `vbr1_l1_binary_weighted_voltage_dac:e2e` | `e2e` | `simple_binary_voltage_dac_4b.va`, `tb_simple_binary_voltage_dac_4b_ref.scs` | `53369ce2063d` |
| `vbr1_l1_binary_weighted_voltage_dac:tb` | `tb` | `tb_simple_binary_voltage_dac_4b_ref.scs` | `bb9e5597b8e0` |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac:bugfix` | `bugfix` | `dut_fixed.va` | `9baf4c177244` |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac:dut` | `dut` | `cdac_cal.va` | `8089cea8c599` |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac:e2e` | `e2e` | `cdac_cal.va`, `tb_cdac_cal_ref.scs` | `5f9a803f7b4f` |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac:tb` | `tb` | `tb_cdac_cal_ref.scs` | `1f5b4f5ad7d8` |
| `vbr1_l1_clocked_adc_quantizer:bugfix` | `bugfix` | `dut_fixed.va` | `317bebc66fe8` |
| `vbr1_l1_clocked_adc_quantizer:dut` | `dut` | `flash_adc_3b.va` | `3af7293ba681` |
| `vbr1_l1_clocked_adc_quantizer:e2e` | `e2e` | `flash_adc_3b.va`, `tb_flash_adc_3b_ref.scs` | `fea727c98d48` |
| `vbr1_l1_clocked_adc_quantizer:tb` | `tb` | `tb_flash_adc_3b_ref.scs` | `9a5c3808a76b` |
| `vbr1_l1_dac_mismatch_unit_weighting_model:bugfix` | `bugfix` | `dut_fixed.va` | `30ce8beb11b0` |
| `vbr1_l1_dac_mismatch_unit_weighting_model:dut` | `dut` | `dac_mismatch_unit_weighting_model.va` | `2eb87c3578e8` |
| `vbr1_l1_dac_mismatch_unit_weighting_model:e2e` | `e2e` | `dac_mismatch_unit_weighting_model.va`, `tb_dac_mismatch_unit_weighting_model.scs` | `b821604ef1b6` |
| `vbr1_l1_dac_mismatch_unit_weighting_model:tb` | `tb` | `tb_dac_mismatch_unit_weighting_model.scs` | `fd60ec47071a` |
| `vbr1_l1_pipeline_adc_stage:bugfix` | `bugfix` | `dut_fixed.va` | `f7fff75347eb` |
| `vbr1_l1_pipeline_adc_stage:dut` | `dut` | `pipeline_stage.va` | `8a1916223021` |
| `vbr1_l1_pipeline_adc_stage:e2e` | `e2e` | `pipeline_stage.va`, `tb_pipeline_stage_ref.scs` | `8db26e55e418` |
| `vbr1_l1_pipeline_adc_stage:tb` | `tb` | `tb_pipeline_stage_ref.scs` | `fa21f2c51d96` |
