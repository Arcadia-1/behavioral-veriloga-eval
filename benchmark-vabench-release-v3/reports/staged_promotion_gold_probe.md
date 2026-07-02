# v3 Staged Promotion Gold Probe

Date: 2026-07-02

## Summary

- `gold_total`: 22
- `gold_pass`: 0
- `gold_fail`: 22
- `expectation_fail`: 22
- `skipped_staged_tasks`: 0
- `wall_s`: 5.290621

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
| `449-generate-genvar-replicated-stage` | `FAIL_DUT_COMPILE` | simulator_error=Failed to compile Verilog-A file generate_genvar_replicated_stage.vams: Parse error at L6:5: Unsupported Verilog-AMS module block 'generate' is outside the EVAS behavioral subset |
| `453-specify-specparam-delay` | `FAIL_DUT_COMPILE` | simulator_error=Failed to compile Verilog-A file specify_specparam_delay.vams: Parse error at L4:5: Unsupported Verilog-AMS module block 'specify' is outside the EVAS behavioral subset |
| `469-current-contribution-conductance` | `FAIL_SIM_CORRECTNESS` | staged_kcl_boundary feature=I(p,n)<+gain*V(p,n) n_range=0 p_range=0.0008 expected=mna_current_observable |
| `470-branch-current-probe-contribution` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.0000 expected_branch_current=0.5000 out@90ns=0.0000 expected_branch_current=0.2000 |
| `471-indirect-branch-null-balance` | `FAIL_SIM_CORRECTNESS` | staged_dynamic_solver_boundary operator=indirect_branch_equation out_range=0 expected=certified_continuous_time_response |
| `472-indirect-branch-ddt-balance` | `FAIL_SIM_CORRECTNESS` | staged_dynamic_solver_boundary operator=indirect_branch_ddt_equation out_range=0 expected=certified_continuous_time_response |
| `481-analog-primitive-resistor-instance` | `FAIL_TB_COMPILE` | simulator_error=Unsupported analog primitive instance: resistor in analog_primitive_resistor_instance.rload; EVAS behavioral mode does not implement conservative analog primitives |
| `482-analog-primitive-isource-instance` | `FAIL_TB_COMPILE` | simulator_error=Unsupported analog primitive instance: isource in analog_primitive_isource_instance.ib; EVAS behavioral mode does not implement conservative analog primitives |
| `491-kcl-capacitor-ddt-current` | `FAIL_SIM_CORRECTNESS` | staged_kcl_boundary feature=I(p,n)<+c*ddt(V(p,n)) p_range=0.0012 expected=mna_current_observable |
| `492-kcl-inductor-idt-voltage` | `FAIL_SIM_CORRECTNESS` | simulator_error=Model isource not found (available: ['kcl_inductor_idt_voltage']) |
| `493-continuous-laplace-nd-filter` | `FAIL_SIM_CORRECTNESS` | staged_dynamic_solver_boundary operator=continuous_laplace_nd out_range=1 expected=certified_continuous_time_response |
| `494-continuous-zi-nd-filter` | `FAIL_SIM_CORRECTNESS` | staged_dynamic_solver_boundary operator=continuous_zi_nd out_range=1 expected=certified_continuous_time_response |
