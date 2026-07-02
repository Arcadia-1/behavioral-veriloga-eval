# v3 Staged Promotion Gold Probe

Date: 2026-07-02

## Summary

- `gold_total`: 7
- `gold_pass`: 0
- `gold_fail`: 7
- `expectation_fail`: 7
- `skipped_staged_tasks`: 0
- `wall_s`: 0.889365

## Rows

| Task | Status | First behavior note |
| --- | --- | --- |
| `444-zi-zp-discrete-filter` | `FAIL_SIM_CORRECTNESS` | staged_dynamic_solver_boundary operator=zi_zp out_range=0.45 metric_range=0.45 expected=certified_continuous_time_response |
| `469-current-contribution-conductance` | `FAIL_SIM_CORRECTNESS` | staged_kcl_boundary feature=I(p,n)<+gain*V(p,n) n_range=0 p_range=0.0008 expected=mna_current_observable |
| `471-indirect-branch-null-balance` | `FAIL_SIM_CORRECTNESS` | staged_dynamic_solver_boundary operator=indirect_branch_equation out_range=0 expected=certified_continuous_time_response |
| `472-indirect-branch-ddt-balance` | `FAIL_SIM_CORRECTNESS` | staged_dynamic_solver_boundary operator=indirect_branch_ddt_equation out_range=0 expected=certified_continuous_time_response |
| `491-kcl-capacitor-ddt-current` | `FAIL_SIM_CORRECTNESS` | staged_kcl_boundary feature=I(p,n)<+c*ddt(V(p,n)) p_range=0.0012 expected=mna_current_observable |
| `493-continuous-laplace-nd-filter` | `FAIL_SIM_CORRECTNESS` | staged_dynamic_solver_boundary operator=continuous_laplace_nd out_range=0.05821 expected=certified_continuous_time_response |
| `494-continuous-zi-nd-filter` | `FAIL_SIM_CORRECTNESS` | staged_dynamic_solver_boundary operator=continuous_zi_nd out_range=1.33 expected=certified_continuous_time_response |
