# bpack-v1 Spectre Audit Report

**Date**: 2026-05-08

## Status

Spectre audit passed on the full `benchmark-bpack-v1/` gold set.

| item | result |
| --- | ---: |
| benchmark | `benchmark-bpack-v1/` |
| tasks | 48 |
| strict-EVAS gold | 48/48 |
| Spectre gold | 48/48 |
| Spectre route | internal bridge profile |
| Spectre version | `21.1.0.509.isr12` |

## Result Roots

- strict-EVAS: `results/bpack-v1-gold-evas-2026-05-07-freeze-candidate/`
- Spectre smoke: `results/bpack-v1-gold-spectre-2026-05-08-han-smoke3/`
- Spectre full audit: `results/bpack-v1-gold-spectre-2026-05-08-han-full/`

The full Spectre summary reports:

| metric | value |
| --- | ---: |
| `pass_count` | 48/48 |
| `dut_compile` | 1.0 |
| `tb_compile` | 1.0 |
| `sim_correct` | 1.0 |
| failures | 0 |

Passes by task form:

| form | pass |
| --- | ---: |
| bugfix | 12/12 |
| spec-to-va/dut | 12/12 |
| end-to-end | 12/12 |
| tb-generation | 12/12 |

## Reproduction

Configure the local Spectre bridge profile for the internal Cadence host, then
run:

```bash
python3 runners/validate_benchmark_v2_gold.py \
  --backend spectre \
  --bench-dir benchmark-bpack-v1 \
  --family bpack-v1 \
  --output-dir results/bpack-v1-gold-spectre-2026-05-08-han-full \
  --timeout-s 240 \
  --profile ci
```

## Interpretation

`bpack-v1` now passes both strict-EVAS and Spectre gold gates.  It can be
promoted from freeze candidate to the frozen `bpack48` benchmark for model
experiments.
