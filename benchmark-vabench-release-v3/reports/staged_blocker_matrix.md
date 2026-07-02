# v3 Staged Blocker Matrix

Date: 2026-07-02

## Summary

- Staged tasks: **5**
- Distinct blocking issues: **1**
- Missing issue links: **0**
- Missing failure summaries: **0**

## Tasks

| Task | Layer | Issue | Probe status | Failure summary | Per-task promotion command |
| --- | --- | --- | --- | --- | --- |
| `469-current-contribution-conductance` | `conservative_kcl_syntax_extension` | https://github.com/Arcadia-1/EVAS/issues/44 | `FAIL_SIM_CORRECTNESS` | staged_kcl_boundary feature=I(p,n)<+gain*V(p,n) n_range=0 p_range=0.0008 expected=mna_current_observable | `PYTHONPATH=runners VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 469 --end 469 --tasks 469 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_task_469.json` |
| `471-indirect-branch-null-balance` | `behavioral_continuous_time_extension` | https://github.com/Arcadia-1/EVAS/issues/44 | `FAIL_SIM_CORRECTNESS` | staged_dynamic_solver_boundary operator=indirect_branch_equation out_range=0 expected=certified_continuous_time_response | `PYTHONPATH=runners VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 471 --end 471 --tasks 471 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_task_471.json` |
| `472-indirect-branch-ddt-balance` | `behavioral_continuous_time_extension` | https://github.com/Arcadia-1/EVAS/issues/44 | `FAIL_SIM_CORRECTNESS` | staged_dynamic_solver_boundary operator=indirect_branch_ddt_equation out_range=0 expected=certified_continuous_time_response | `PYTHONPATH=runners VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 472 --end 472 --tasks 472 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_task_472.json` |
| `491-kcl-capacitor-ddt-current` | `conservative_kcl_syntax_extension` | https://github.com/Arcadia-1/EVAS/issues/44 | `FAIL_SIM_CORRECTNESS` | staged_kcl_boundary feature=I(p,n)<+c*ddt(V(p,n)) p_range=0.0012 expected=mna_current_observable | `PYTHONPATH=runners VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 491 --end 491 --tasks 491 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_task_491.json` |
| `494-continuous-zi-nd-filter` | `behavioral_continuous_time_extension` | https://github.com/Arcadia-1/EVAS/issues/44 | `FAIL_SIM_CORRECTNESS` | staged_dynamic_solver_boundary operator=continuous_zi_nd out_range=1.33 expected=certified_continuous_time_response | `PYTHONPATH=runners VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 494 --end 494 --tasks 494 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_task_494.json` |
