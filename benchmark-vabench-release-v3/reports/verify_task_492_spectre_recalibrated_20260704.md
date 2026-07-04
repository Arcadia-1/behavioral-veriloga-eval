# v3 Staged Promotion Gold Probe

Date: 2026-07-04

## Summary

- `gold_total`: 1
- `gold_pass`: 1
- `gold_fail`: 0
- `expectation_fail`: 0
- `skipped_staged_tasks`: 0
- `gold_wall_s_total`: 0.321733
- `gold_wall_s_max`: 0.321733
- `slow_gold_threshold_s`: 20.0
- `slow_gold_count`: 0
- `wall_s`: 1.323043

## Gold Timing Top 20

| Task | Status | Wall s |
| --- | --- | ---: |
| `492-kcl-inductor-idt-voltage` | `PASS` | 0.321733 |

## Rows

| Task | Status | First behavior note |
| --- | --- | --- |
| `492-kcl-inductor-idt-voltage` | `PASS` |  |
| `492-kcl-inductor-idt-voltage` | `FAIL_SIM_CORRECTNESS` | p@21ns=0.000e+00 expected=-5.000e-25 tol=2.500e-25 p@40ns=0.000e+00 expected=-1.950e-23 tol=5.850e-25 p@80ns=0.000e+00 expected=-5.950e-23 tol=1.785e-24 p@100ns=0.000e+00 expected=-4.050e-23 tol=1.215e-24 |
| `492-kcl-inductor-idt-voltage` | `FAIL_SIM_CORRECTNESS` | p@21ns=-1.000e-24 expected=-5.000e-25 tol=2.500e-25 p@40ns=-3.900e-23 expected=-1.950e-23 tol=5.850e-25 p@80ns=-1.190e-22 expected=-5.950e-23 tol=1.785e-24 p@100ns=-8.100e-23 expected=-4.050e-23 tol=1.215e-24 |
| `492-kcl-inductor-idt-voltage` | `FAIL_SIM_CORRECTNESS` | p@21ns=5.000e-25 expected=-5.000e-25 tol=2.500e-25 p@40ns=1.950e-23 expected=-1.950e-23 tol=5.850e-25 p@80ns=5.950e-23 expected=-5.950e-23 tol=1.785e-24 p@100ns=4.050e-23 expected=-4.050e-23 tol=1.215e-24 |
| `492-kcl-inductor-idt-voltage` | `FAIL_SIM_CORRECTNESS` | p@21ns=1.000e-10 expected=-5.000e-25 tol=2.500e-25 p@40ns=1.000e-10 expected=-1.950e-23 tol=5.850e-25 p@80ns=1.000e-10 expected=-5.950e-23 tol=1.785e-24 p@100ns=1.000e-10 expected=-4.050e-23 tol=1.215e-24 |
| `492-kcl-inductor-idt-voltage` | `FAIL_SIM_CORRECTNESS` | p@40ns=-1.560e-23 expected=-1.950e-23 tol=5.850e-25 p@80ns=-4.760e-23 expected=-5.950e-23 tol=1.785e-24 p@100ns=-3.240e-23 expected=-4.050e-23 tol=1.215e-24 p@120ns=-1.640e-23 expected=-2.050e-23 tol=6.150e-25 |
