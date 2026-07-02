# v3 Staged Promotion Gold Probe

Date: 2026-07-02

## Summary

- `gold_total`: 16
- `gold_pass`: 0
- `gold_fail`: 16
- `expectation_fail`: 16
- `skipped_staged_tasks`: 0
- `wall_s`: 2.111231

## Rows

| Task | Status | First behavior note |
| --- | --- | --- |
| `435-ddt-voltage-derivative-source` | `FAIL_SIM_CORRECTNESS` | staged_dynamic_solver_boundary operator=ddt out_range=8.653e+05 metric_range=8.653e+05 expected=certified_continuous_time_response |
| `436-idt-voltage-integrator-source` | `FAIL_SIM_CORRECTNESS` | staged_dynamic_solver_boundary operator=idt out_range=7.5e-08 metric_range=7.5e-08 expected=certified_continuous_time_response |
| `437-laplace-nd-lowpass-filter` | `FAIL_SIM_CORRECTNESS` | staged_dynamic_solver_boundary operator=laplace_nd out_range=0.8 metric_range=0.8 expected=certified_continuous_time_response |
| `438-laplace-np-pole-filter` | `FAIL_SIM_CORRECTNESS` | staged_dynamic_solver_boundary operator=laplace_np out_range=0.6 metric_range=0.6 expected=certified_continuous_time_response |
| `439-laplace-zd-zero-den-filter` | `FAIL_SIM_CORRECTNESS` | staged_dynamic_solver_boundary operator=laplace_zd out_range=0.75 metric_range=0.75 expected=certified_continuous_time_response |
| `440-laplace-zp-zero-pole-filter` | `FAIL_SIM_CORRECTNESS` | staged_dynamic_solver_boundary operator=laplace_zp out_range=0.9 metric_range=0.9 expected=certified_continuous_time_response |
| `441-zi-nd-discrete-filter` | `FAIL_SIM_CORRECTNESS` | staged_dynamic_solver_boundary operator=zi_nd out_range=0.7 metric_range=0.7 expected=certified_continuous_time_response |
| `442-zi-np-discrete-filter` | `FAIL_SIM_CORRECTNESS` | staged_dynamic_solver_boundary operator=zi_np out_range=0.65 metric_range=0.65 expected=certified_continuous_time_response |
| `443-zi-zd-discrete-filter` | `FAIL_SIM_CORRECTNESS` | staged_dynamic_solver_boundary operator=zi_zd out_range=0.85 metric_range=0.85 expected=certified_continuous_time_response |
| `444-zi-zp-discrete-filter` | `FAIL_SIM_CORRECTNESS` | staged_dynamic_solver_boundary operator=zi_zp out_range=0.45 metric_range=0.45 expected=certified_continuous_time_response |
| `469-current-contribution-conductance` | `FAIL_SIM_CORRECTNESS` | staged_kcl_boundary feature=I(p,n)<+gain*V(p,n) n_range=0 p_range=0.0008 expected=mna_current_observable |
| `471-indirect-branch-null-balance` | `FAIL_SIM_CORRECTNESS` | staged_dynamic_solver_boundary operator=indirect_branch_equation out_range=0 expected=certified_continuous_time_response |
| `472-indirect-branch-ddt-balance` | `FAIL_SIM_CORRECTNESS` | staged_dynamic_solver_boundary operator=indirect_branch_ddt_equation out_range=0 expected=certified_continuous_time_response |
| `491-kcl-capacitor-ddt-current` | `FAIL_SIM_CORRECTNESS` | staged_kcl_boundary feature=I(p,n)<+c*ddt(V(p,n)) p_range=0.0012 expected=mna_current_observable |
| `493-continuous-laplace-nd-filter` | `FAIL_SIM_CORRECTNESS` | staged_dynamic_solver_boundary operator=continuous_laplace_nd out_range=1 expected=certified_continuous_time_response |
| `494-continuous-zi-nd-filter` | `FAIL_SIM_CORRECTNESS` | staged_dynamic_solver_boundary operator=continuous_zi_nd out_range=1 expected=certified_continuous_time_response |
