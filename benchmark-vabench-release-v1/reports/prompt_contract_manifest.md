# vaBench Release Prompt Contract Manifest

Date: 2026-05-22

| Metric | Value |
| --- | ---: |
| status | `pass` |
| prompt version | `public-contract-v2` |
| prompts | 259 |

## Form Counts

| Form | Prompts |
| --- | ---: |
| `bugfix` | 52 |
| `dut` | 57 |
| `e2e` | 75 |
| `tb` | 75 |

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
| `vbr1_l1_aperture_delay_track_and_hold:bugfix` | `bugfix` | `dut_fixed.va` | `450d46d8b8ee` |
| `vbr1_l1_aperture_delay_track_and_hold:dut` | `dut` | `sample_hold_aperture_ref.va` | `e950eff8efef` |
| `vbr1_l1_aperture_delay_track_and_hold:e2e` | `e2e` | `sample_hold_aperture_ref.va`, `tb_sample_hold_aperture_ref.scs` | `335e4d00b496` |
| `vbr1_l1_aperture_delay_track_and_hold:tb` | `tb` | `tb_sample_hold_aperture_ref.scs` | `fcdbfb01c5f5` |
| `vbr1_l1_bang_bang_phase_detector:bugfix` | `bugfix` | `dut_fixed.va` | `12b9eb54c386` |
| `vbr1_l1_bang_bang_phase_detector:dut` | `dut` | `bbpd_ref.va` | `549e0d006cde` |
| `vbr1_l1_bang_bang_phase_detector:e2e` | `e2e` | `bbpd_data_edge_alignment_ref.va`, `tb_bbpd_data_edge_alignment_ref.scs` | `80cc22e846fc` |
| `vbr1_l1_bang_bang_phase_detector:tb` | `tb` | `tb_bbpd_data_edge_alignment_ref.scs` | `e48334ba3cbb` |
| `vbr1_l1_binary_weighted_voltage_dac:bugfix` | `bugfix` | `dut_fixed.va` | `f16d04c7bff8` |
| `vbr1_l1_binary_weighted_voltage_dac:dut` | `dut` | `simple_binary_voltage_dac_4b.va` | `3ef431690cca` |
| `vbr1_l1_binary_weighted_voltage_dac:e2e` | `e2e` | `simple_binary_voltage_dac_4b.va`, `tb_simple_binary_voltage_dac_4b_ref.scs` | `d14d20651a93` |
| `vbr1_l1_binary_weighted_voltage_dac:tb` | `tb` | `tb_simple_binary_voltage_dac_4b_ref.scs` | `ac8e84b74d45` |
| `vbr1_l1_burst_clock_source:dut` | `dut` | `clk_burst_gen.va` | `85bb9702ec8e` |
| `vbr1_l1_burst_clock_source:e2e` | `e2e` | `clk_burst_gen.va`, `tb_clk_burst_gen_ref.scs` | `9e668ab307f5` |
| `vbr1_l1_burst_clock_source:tb` | `tb` | `tb_clk_burst_gen_ref.scs` | `b3d40d37f665` |
| `vbr1_l1_calibration_deadband_controller:bugfix` | `bugfix` | `dut_fixed.va` | `61060e8cafe0` |
| `vbr1_l1_calibration_deadband_controller:dut` | `dut` | `calibration_deadband_controller.va` | `89abdcafcf19` |
| `vbr1_l1_calibration_deadband_controller:e2e` | `e2e` | `calibration_deadband_controller.va`, `tb_calibration_deadband_controller.scs` | `53f9f22f70c5` |
| `vbr1_l1_calibration_deadband_controller:tb` | `tb` | `tb_calibration_deadband_controller.scs` | `6bd13096bdbb` |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac:bugfix` | `bugfix` | `dut_fixed.va` | `ca3a0022605b` |
