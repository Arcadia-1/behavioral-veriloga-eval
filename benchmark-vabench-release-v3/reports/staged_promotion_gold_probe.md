# v3 Staged Promotion Gold Probe

Date: 2026-07-02

## Summary

- `gold_total`: 36
- `gold_pass`: 0
- `gold_fail`: 36
- `expectation_fail`: 36
- `skipped_staged_tasks`: 0
- `wall_s`: 9.612872

## Rows

| Task | Status | First behavior note |
| --- | --- | --- |
| `353-always-resettable-toggle` | `FAIL_SIM_CORRECTNESS` | q@50ns=0.0000 expected=1.0000 tol=0.0800 |
| `410-macro-ifdef-gain-select` | `FAIL_SIM_CORRECTNESS` | out@160ns=0.4800 expected=0.8000 tol=0.0800 |
| `415-logic-vector-assign-slice` | `FAIL_SIM_CORRECTNESS` | y@50ns=0.0000 expected=1.0000 tol=0.0800 |
| `416-logic-vector-reduction-flag` | `FAIL_SIM_CORRECTNESS` | valid@50ns=0.0000 expected=1.0000 tol=0.0800 |
| `417-always-async-reset-counter` | `FAIL_SIM_CORRECTNESS` | q@100ns=0.0000 expected=1.0000 tol=0.0800 |
| `418-always-enable-saturating-counter` | `FAIL_SIM_CORRECTNESS` | q0@90ns=0.0000 expected=1.0000 tol=0.0800 |
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
| `449-generate-genvar-replicated-stage` | `FAIL_SIM_CORRECTNESS` | y@10ns=0.0000 expected=0.8000 tol=0.0500 |
| `453-specify-specparam-delay` | `FAIL_SIM_CORRECTNESS` | staged_specify_boundary a_range=1 y_range=1 expected=certified_specify_path_delay |
| `455-packed-logic-bus-slice` | `FAIL_SIM_CORRECTNESS` | y3@50ns=0.0000 expected_a7=1.0000 y1@50ns=0.0000 expected_a1=1.0000 y0@50ns=0.0000 expected_a0=1.0000 y3@90ns=0.0000 expected_a7=1.0000 |
| `464-param-given-gain-select` | `FAIL_SIM_CORRECTNESS` | out_ovr@12ns=0.6000 expected=0.3000 metric_ovr@12ns=0.0000 expected=1.0000 out_ovr@52ns=0.3000 expected=0.1500 metric_ovr@52ns=0.0000 expected=1.0000 |
| `468-branch-declaration-voltage-probe` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.0000 expected=0.1000 tol=0.0350 |
| `469-current-contribution-conductance` | `FAIL_SIM_CORRECTNESS` | staged_kcl_boundary feature=I(p,n)<+gain*V(p,n) n_range=0 p_range=0.0008 expected=mna_current_observable |
| `470-branch-current-probe-contribution` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.0000 expected_branch_current=0.5000 out@90ns=0.0000 expected_branch_current=0.2000 |
| `471-indirect-branch-null-balance` | `FAIL_SIM_CORRECTNESS` | staged_dynamic_solver_boundary operator=indirect_branch_equation out_range=0 expected=certified_continuous_time_response |
| `472-indirect-branch-ddt-balance` | `FAIL_SIM_CORRECTNESS` | staged_dynamic_solver_boundary operator=indirect_branch_ddt_equation out_range=0 expected=certified_continuous_time_response |
| `476-oomr-string-voltage-probe` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.0000 expected=0.2000 tol=0.0350 |
| `477-analog-node-alias-initial` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.0000 expected=0.2000 tol=0.0350 |
| `480-mfactor-system-function-gain` | `FAIL_DUT_COMPILE` | simulator_error=Failed to compile Verilog-A file mfactor_system_function_gain.va: Spectre-incompatible/unsupported Verilog-A function call: $mfactor() |
| `481-analog-primitive-resistor-instance` | `FAIL_TB_COMPILE` | simulator_error=Unknown child module: resistor in analog_primitive_resistor_instance.rload |
| `482-analog-primitive-isource-instance` | `FAIL_TB_COMPILE` | simulator_error=Unknown child module: isource in analog_primitive_isource_instance.ib |
| `487-table-model-2d-array-surface` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.0000 expected=1.0000 tol=0.0500 |
| `488-table-model-string-param-source` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.0000 expected=0.1000 tol=0.0400 |
| `491-kcl-capacitor-ddt-current` | `FAIL_SIM_CORRECTNESS` | staged_kcl_boundary feature=I(p,n)<+c*ddt(V(p,n)) p_range=0.0012 expected=mna_current_observable |
| `492-kcl-inductor-idt-voltage` | `FAIL_SIM_CORRECTNESS` | simulator_error=evas completed with 1 error but did not expose a detailed diagnostic in captured output |
| `493-continuous-laplace-nd-filter` | `FAIL_SIM_CORRECTNESS` | staged_dynamic_solver_boundary operator=continuous_laplace_nd out_range=1 expected=certified_continuous_time_response |
| `494-continuous-zi-nd-filter` | `FAIL_SIM_CORRECTNESS` | staged_dynamic_solver_boundary operator=continuous_zi_nd out_range=1 expected=certified_continuous_time_response |
