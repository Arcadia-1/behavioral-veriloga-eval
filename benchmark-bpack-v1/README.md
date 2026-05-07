# bpack-v1 Benchmark Draft

This benchmark root is materialized from `docs/BPACK_V1_INVENTORY.json`.
Its unit of balance is a concrete `circuit_function_id` pack with four task forms:
`bugfix`, `spec-to-va`, `end-to-end`, and `tb-generation`.

## Current Status

- Packs in inventory: 12
- Materialized tasks: 48
- Authored bpack tasks: 20
- Complete packs by referenced forms: 12
- Exact seed packs: 4

This is a draft benchmark root.  Tasks whose `promotion_status` contains
`draft` or `needs_contract_review` must not be treated as frozen bpack-v1
tasks until gold validation and contract review pass.

## Form Counts

| form | tasks |
| --- | ---: |
| `bugfix` | 12 |
| `spec-to-va` | 12 |
| `end-to-end` | 12 |
| `tb-generation` | 12 |

## Packs

| pack | status | missing forms |
| --- | --- | --- |
| `threshold_detector` | `existing_exact_pack` | -; authored=- |
| `window_detector` | `existing_exact_pack` | -; authored=- |
| `analog_limiter` | `existing_exact_pack` | -; authored=- |
| `pulse_stretcher` | `existing_exact_pack` | -; authored=- |
| `sample_hold` | `existing_needs_contract_review` | -; authored=spec-to-va |
| `pfd_updn` | `existing_needs_contract_review` | -; authored=spec-to-va, tb-generation |
| `binary_dac_4b` | `existing_needs_contract_review` | -; authored=bugfix, spec-to-va |
| `clock_divider` | `needs_authoring` | -; authored=bugfix, spec-to-va, tb-generation |
| `hysteresis_comparator` | `needs_authoring` | -; authored=bugfix, spec-to-va, tb-generation |
| `flash_adc_3b` | `needs_authoring` | -; authored=bugfix, spec-to-va, tb-generation |
| `dwa_pointer` | `needs_authoring` | -; authored=bugfix, spec-to-va, tb-generation |
| `prbs7_lfsr` | `needs_authoring` | -; authored=bugfix, end-to-end, tb-generation |
