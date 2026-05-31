# DeepSeek Eventfix9 Latest Conclusion (2026-05-29)
## Scope
- Benchmark: vaBench release v1 scored 236 forms.
- EVAS: current eventfix9 core with exact-touch future-probe semantics and RF mixer time-weighted checker.
- Spectre backend: `sui-direct` on `thu-wei`.
- Final judge: Spectre; strict dual pass requires EVAS and Spectre agreement.

## Results
| View | Spectre Pass | Strict Dual Pass | Full Rate | Completed/Materialized | EVAS->Spectre | Spectre->EVAS |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| DeepSeek raw same-candidates | 52/236 | 52/236 | 22.0% | 232 completed, 4 incomplete | 0 | 0 |
| DeepSeek latest overlay | 59/236 | 59/236 | 25.0% | 236 materialized, 4 incomplete | 0 | 0 |
| MiMo reference eventfix7 | 51/236 | 51/236 | 21.6% | 212 completed, 24 skipped | 0 | 0 |

## DeepSeek Latest Overlay By Form
| Form | Total | Spectre Pass | Strict Dual Pass |
| --- | ---: | ---: | ---: |
| `bugfix` | 52 | 13 | 13 |
| `dut` | 52 | 19 | 19 |
| `e2e` | 66 | 10 | 10 |
| `tb` | 66 | 17 | 17 |

## Conclusion
- Eventfix9 removes all observed EVAS/Spectre direction mismatches for DeepSeek: both `EVAS PASS / Spectre FAIL` and `Spectre PASS / EVAS FAIL` are zero.
- The raw same-candidate DeepSeek score is `52/236 = 22.0%`; the latest overlay score remains `59/236 = 25.0%` because it includes later regenerated wrapper-v4/v5 candidates.
- Since strict dual pass now equals Spectre pass, remaining non-pass rows should be analyzed as model output failures or incomplete generations, not evaluator parity debt.
