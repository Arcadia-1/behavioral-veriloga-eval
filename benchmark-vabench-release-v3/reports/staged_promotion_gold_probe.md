# v3 Staged Promotion Gold Probe

Date: 2026-07-02

## Summary

- `gold_total`: 36
- `gold_pass`: 0
- `gold_fail`: 36
- `expectation_fail`: 36
- `skipped_staged_tasks`: 0
- `wall_s`: 8.264613

## Rows

| Task | Status | First behavior note |
| --- | --- | --- |
| `353-always-resettable-toggle` | `FAIL_SIM_CORRECTNESS` | q@50ns=0.0000 expected=1.0000 tol=0.0800 |
| `410-macro-ifdef-gain-select` | `FAIL_SIM_CORRECTNESS` | out@160ns=0.4800 expected=0.8000 tol=0.0800 |
| `415-logic-vector-assign-slice` | `FAIL_SIM_CORRECTNESS` | y@50ns=0.0000 expected=1.0000 tol=0.0800 |
| `416-logic-vector-reduction-flag` | `FAIL_SIM_CORRECTNESS` | valid@50ns=0.0000 expected=1.0000 tol=0.0800 |
| `417-always-async-reset-counter` | `FAIL_SIM_CORRECTNESS` | q@100ns=0.0000 expected=1.0000 tol=0.0800 |
| `418-always-enable-saturating-counter` | `FAIL_SIM_CORRECTNESS` | q0@90ns=0.0000 expected=1.0000 tol=0.0800 |
| `435-ddt-voltage-derivative-source` | `FAIL_SIM_CORRECTNESS` | no behavior check implemented for v3_435_ddt_voltage_derivative_source |
| `436-idt-voltage-integrator-source` | `FAIL_SIM_CORRECTNESS` | no behavior check implemented for v3_436_idt_voltage_integrator_source |
| `437-laplace-nd-lowpass-filter` | `FAIL_SIM_CORRECTNESS` | no behavior check implemented for v3_437_laplace_nd_lowpass_filter |
| `438-laplace-np-pole-filter` | `FAIL_SIM_CORRECTNESS` | no behavior check implemented for v3_438_laplace_np_pole_filter |
| `439-laplace-zd-zero-den-filter` | `FAIL_SIM_CORRECTNESS` | no behavior check implemented for v3_439_laplace_zd_zero_den_filter |
| `440-laplace-zp-zero-pole-filter` | `FAIL_SIM_CORRECTNESS` | no behavior check implemented for v3_440_laplace_zp_zero_pole_filter |
| `441-zi-nd-discrete-filter` | `FAIL_SIM_CORRECTNESS` | no behavior check implemented for v3_441_zi_nd_discrete_filter |
| `442-zi-np-discrete-filter` | `FAIL_SIM_CORRECTNESS` | no behavior check implemented for v3_442_zi_np_discrete_filter |
| `443-zi-zd-discrete-filter` | `FAIL_SIM_CORRECTNESS` | no behavior check implemented for v3_443_zi_zd_discrete_filter |
| `444-zi-zp-discrete-filter` | `FAIL_SIM_CORRECTNESS` | no behavior check implemented for v3_444_zi_zp_discrete_filter |
| `449-generate-genvar-replicated-stage` | `FAIL_SIM_CORRECTNESS` | y@10ns=0.0000 expected=0.8000 tol=0.0500 |
| `453-specify-specparam-delay` | `FAIL_SIM_CORRECTNESS` | no behavior check implemented for v3_453_specify_specparam_delay |
| `455-packed-logic-bus-slice` | `FAIL_SIM_CORRECTNESS` | missing_columns=y0,y3 |
| `464-param-given-gain-select` | `FAIL_SIM_CORRECTNESS` | out_ovr@12ns=0.6000 expected=0.3000 metric_ovr@12ns=0.0000 expected=1.0000 out_ovr@52ns=0.3000 expected=0.1500 metric_ovr@52ns=0.0000 expected=1.0000 |
| `468-branch-declaration-voltage-probe` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.0000 expected=0.1000 tol=0.0350 |
| `469-current-contribution-conductance` | `FAIL_SIM_CORRECTNESS` | no behavior check implemented for v3_469_current_contribution_conductance |
| `470-branch-current-probe-contribution` | `FAIL_SIM_CORRECTNESS` | no behavior check implemented for v3_470_branch_current_probe_contribution |
| `471-indirect-branch-null-balance` | `FAIL_SIM_CORRECTNESS` | no behavior check implemented for v3_471_indirect_branch_null_balance |
| `472-indirect-branch-ddt-balance` | `FAIL_SIM_CORRECTNESS` | no behavior check implemented for v3_472_indirect_branch_ddt_balance |
| `476-oomr-string-voltage-probe` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.0000 expected=0.2000 tol=0.0350 |
| `477-analog-node-alias-initial` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.0000 expected=0.2000 tol=0.0350 |
| `480-mfactor-system-function-gain` | `FAIL_DUT_COMPILE` | dut_not_compiled |
| `481-analog-primitive-resistor-instance` | `FAIL_TB_COMPILE` | tb_not_executed |
| `482-analog-primitive-isource-instance` | `FAIL_TB_COMPILE` | tb_not_executed |
| `487-table-model-2d-array-surface` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.0000 expected=1.0000 tol=0.0500 |
| `488-table-model-string-param-source` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.0000 expected=0.1000 tol=0.0400 |
| `491-kcl-capacitor-ddt-current` | `FAIL_SIM_CORRECTNESS` | no behavior check implemented for v3_491_kcl_capacitor_ddt_current |
| `492-kcl-inductor-idt-voltage` | `FAIL_SIM_CORRECTNESS` | tran.csv missing |
| `493-continuous-laplace-nd-filter` | `FAIL_SIM_CORRECTNESS` | no behavior check implemented for v3_493_continuous_laplace_nd_filter |
| `494-continuous-zi-nd-filter` | `FAIL_SIM_CORRECTNESS` | no behavior check implemented for v3_494_continuous_zi_nd_filter |
