# bpack-v1 Freeze Report

**Date**: 2026-05-08

## Summary

| item | value |
| --- | ---: |
| packs | 12 |
| tasks | 48 |
| authored task forms | 20 |
| bugfix/spec/end-to-end/tb-generation | 12 / 12 / 12 / 12 |
| strict-EVAS gold | 48/48 |
| Spectre gold | 48/48 |

`benchmark-bpack-v1/` is now a frozen bpack48 benchmark: 12 concrete circuit-function packs x 4 task forms.  All 48 gold tasks pass both strict-EVAS and Spectre.

## Contract Cleanup Decisions

| pack | previous issue | freeze-candidate decision | authored forms |
| --- | --- | --- | --- |
| `threshold_detector` | No issue; exact seed pack. | Carry forward existing exact four-form pack. | - |
| `window_detector` | No issue; exact seed pack. | Carry forward existing exact four-form pack. | - |
| `analog_limiter` | No issue; exact seed pack. | Carry forward existing exact four-form pack. | - |
| `pulse_stretcher` | No issue; exact seed pack. | Carry forward existing exact four-form pack. | - |
| `sample_hold` | Spec task used droop variant rather than plain sample-hold. | Use plain `sample_hold_smoke` as canonical source for authored spec-to-va. | `spec-to-va` |
| `pfd_updn` | Spec/TB candidates mixed BBPD/XOR with PFD UP/DN. | Use `pfd_updn_smoke` as canonical source for authored spec-to-va and TB. | `spec-to-va`, `tb-generation` |
| `binary_dac_4b` | Bugfix/spec candidates mixed CDAC/segmented DAC with binary 4-bit DAC. | Use `dac_binary_clk_4b_smoke` as canonical source for authored bugfix and spec-to-va. | `bugfix`, `spec-to-va` |
| `clock_divider` | Existing candidates mixed programmable divider and minimal divider. | Use divide-by-4 `clk_div_smoke` as canonical source for authored missing/contract forms. | `bugfix`, `spec-to-va`, `tb-generation` |
| `hysteresis_comparator` | Existing bugfix/spec candidates were generic flag/comparator-delay tasks. | Use `comparator_hysteresis_smoke` as canonical source for authored forms. | `bugfix`, `spec-to-va`, `tb-generation` |
| `flash_adc_3b` | Only end-to-end existed. | Derive missing forms from `flash_adc_3b_smoke`. | `bugfix`, `spec-to-va`, `tb-generation` |
| `dwa_pointer` | Candidates mixed BG calibration and DWA pointer/no-overlap variants. | Use `dwa_ptr_gen_smoke` as the canonical DWA pointer source for authored forms. | `bugfix`, `spec-to-va`, `tb-generation` |
| `prbs7_lfsr` | Existing end-to-end was 31-bit LFSR, not PRBS7. | Use `prbs7` as canonical source and author bugfix/e2e/TB forms. | `bugfix`, `end-to-end`, `tb-generation` |

## Validation

- strict-EVAS gold result root: `results/bpack-v1-gold-evas-2026-05-07-freeze-candidate/`
- Spectre gold result root: `results/bpack-v1-gold-spectre-2026-05-08-han-full/`
- result: strict-EVAS `48/48 PASS`; Spectre `48/48 PASS`
- all authored task forms are represented in `benchmark-bpack-v1/manifest.json` with `bpack_authored=true`

## Next Gate

1. Launch model experiments on the frozen benchmark: `prompt-only`, `rules-only/D`, `compile-loop/C`, `compile-skill-advanced`.
2. Report task-level and pack-level metrics for every condition.
3. Use the residual taxonomy from the main chain to decide whether behavior-oriented conditions should be added later.

## Known Risk

Some authored tasks are derived from multi-module gold sources, especially `dwa_pointer`.  Gold validation is clean, but model-generation runners should be checked for multi-module bugfix extraction before using these rows in final model tables.
