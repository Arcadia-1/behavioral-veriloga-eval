# Prompt Change Rerun Results 20260529

- Rerun scope: 53/236 scored forms
- Scope manifest: `benchmark-vabench-release-v1/reports/prompt_change_rerun_manifest_20260529.json`
- Task id file: `benchmark-vabench-release-v1/reports/prompt_change_rerun_task_ids_20260529.txt`

## Checker Note

RF mixer activity metric threshold relaxed from 0.45 V to 0.40 V to avoid half-duty-cycle Spectre/EVAS boundary jitter while still rejecting missing/weak activity metrics. Regression added in tests/test_vabench_function_checker_regressions.py.

## Current Full-236 Overlay

| Model | Rerun dual pass | Rerun EVAS P/S F | Rerun Spectre P/EVAS F | Full strict dual pass | Full strict rate | Full EVAS P/S F | Full Spectre P/EVAS F | Incomplete | Runner inconclusive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `deepseek-v4-pro` | 14/53 | 0 | 2 | 66/236 | 27.97% | 0 | 2 | 14 | 0 |
| `mimo-v2.5-pro` | 7/53 | 0 | 3 | 55/236 | 23.31% | 0 | 3 | 23 | 6 |

## Sources

- `deepseek-v4-pro` prompt-only: `results/vabench-release-v1-baseline-minimax-deepseek-v4-pro-20260529-prompt-change-rerun53`; rerun dual: `results/vabench-release-v1-baseline-dual-deepseek-v4-pro-20260529-prompt-change-rerun53-dual`; overlay: `benchmark-vabench-release-v1/reports/evas_spectre_mismatch_triage_deepseek_eventfix9_prompt_change_overlay_20260529.json`
- `mimo-v2.5-pro` prompt-only: `results/vabench-release-v1-baseline-minimax-mimo-v2.5-pro-20260529-prompt-change-rerun53`; rerun dual: `results/vabench-release-v1-baseline-dual-mimo-v2.5-pro-20260529-prompt-change-rerun53-dual`; overlay: `benchmark-vabench-release-v1/reports/evas_spectre_mismatch_triage_mimo_v25pro_prompt_change_overlay_20260529.json`
