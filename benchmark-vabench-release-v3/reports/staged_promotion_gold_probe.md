# v3 Staged Promotion Gold Probe

Date: 2026-07-02

## Summary

- `gold_total`: 2
- `gold_pass`: 0
- `gold_fail`: 2
- `expectation_fail`: 2
- `skipped_staged_tasks`: 0
- `wall_s`: 0.464181

## Rows

| Task | Status | First behavior note |
| --- | --- | --- |
| `469-current-contribution-conductance` | `FAIL_SIM_CORRECTNESS` | staged_kcl_boundary feature=I(p,n)<+gain*V(p,n) n_range=0 p_range=0.0008 expected=mna_current_observable |
| `491-kcl-capacitor-ddt-current` | `FAIL_SIM_CORRECTNESS` | staged_kcl_boundary feature=I(p,n)<+c*ddt(V(p,n)) p_range=0.0012 expected=mna_current_observable |
