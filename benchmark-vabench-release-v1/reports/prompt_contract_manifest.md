# vaBench Release Prompt Contract Manifest

Date: 2026-05-24

| Metric | Value |
| --- | ---: |
| status | `pass` |
| prompt version | `public-contract-v2` |
| prompts | 245 |

## Form Counts

| Form | Prompts |
| --- | ---: |
| `bugfix` | 48 |
| `dut` | 53 |
| `e2e` | 72 |
| `tb` | 72 |

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
| `vbr1_l1_adc_code_capture_register:bugfix` | `bugfix` | `dut_fixed.va` | `50e662d25ca1` |
| `vbr1_l1_adc_code_capture_register:dut` | `dut` | `adc_code_capture_register.va` | `0a0d4b350077` |
| `vbr1_l1_adc_code_capture_register:e2e` | `e2e` | `adc_code_capture_register.va`, `tb_adc_code_capture_register.scs` | `a2377721babd` |
| `vbr1_l1_adc_code_capture_register:tb` | `tb` | `tb_adc_code_capture_register.scs` | `0913842d700b` |
| `vbr1_l1_binary_weighted_voltage_dac:bugfix` | `bugfix` | `dut_fixed.va` | `b160b094d220` |
| `vbr1_l1_binary_weighted_voltage_dac:dut` | `dut` | `simple_binary_voltage_dac_4b.va` | `de33f0420d9d` |
| `vbr1_l1_binary_weighted_voltage_dac:e2e` | `e2e` | `simple_binary_voltage_dac_4b.va`, `tb_simple_binary_voltage_dac_4b_ref.scs` | `3c1ac9a5fedc` |
| `vbr1_l1_binary_weighted_voltage_dac:tb` | `tb` | `tb_simple_binary_voltage_dac_4b_ref.scs` | `1ae314b106f4` |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac:bugfix` | `bugfix` | `dut_fixed.va` | `ca3a0022605b` |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac:dut` | `dut` | `cdac_cal.va` | `1284da6b93bc` |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac:e2e` | `e2e` | `cdac_cal.va`, `tb_cdac_cal_ref.scs` | `b85127d02984` |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac:tb` | `tb` | `tb_cdac_cal_ref.scs` | `44a032568cb7` |
| `vbr1_l1_clocked_adc_quantizer:bugfix` | `bugfix` | `dut_fixed.va` | `317bebc66fe8` |
| `vbr1_l1_clocked_adc_quantizer:dut` | `dut` | `flash_adc_3b.va` | `3af7293ba681` |
| `vbr1_l1_clocked_adc_quantizer:e2e` | `e2e` | `flash_adc_3b.va`, `tb_flash_adc_3b_ref.scs` | `3961de76c42a` |
| `vbr1_l1_clocked_adc_quantizer:tb` | `tb` | `tb_flash_adc_3b_ref.scs` | `9a5c3808a76b` |
| `vbr1_l1_dac_mismatch_unit_weighting_model:bugfix` | `bugfix` | `dut_fixed.va` | `30ce8beb11b0` |
| `vbr1_l1_dac_mismatch_unit_weighting_model:dut` | `dut` | `dac_mismatch_unit_weighting_model.va` | `2eb87c3578e8` |
| `vbr1_l1_dac_mismatch_unit_weighting_model:e2e` | `e2e` | `dac_mismatch_unit_weighting_model.va`, `tb_dac_mismatch_unit_weighting_model.scs` | `b821604ef1b6` |
| `vbr1_l1_dac_mismatch_unit_weighting_model:tb` | `tb` | `tb_dac_mismatch_unit_weighting_model.scs` | `fd60ec47071a` |
