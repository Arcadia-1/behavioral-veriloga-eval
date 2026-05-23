# CT05 Dual Closure - 2026-05-23

- Scope: `CT05_pll_clock_event_timing`
- Status: `complete`
- Queue forms: `46`; executed bundles: `56` with `8` workers
- Expected-met: `56/56`; expected-miss: `0`
- Primary pass: `46/46`
- Buggy companions caught: `10/10`
- CT05 imported dual certification: `46` forms, status counts `{'pass': 46}`
- CT05 EVAS PASS / Spectre FAIL: `0`

## Evidence

- Rerun summary: `results/ct05-dual-rerun-20260523-final/summary.json`
- Queue: `benchmark-vabench-release-v1/reports/ct05_dual_rerun_queue_20260523.json`
- Import report: `benchmark-vabench-release-v1/reports/dual_rerun_import.json`

## Checker Closure

- BBPD bugfix companion now checks UP/DOWN direction against `clk` and `retimed_data`, not just pulse presence.
- Regression: `tests/test_vabench_function_checker_regressions.py::test_bbpd_checker_rejects_swapped_up_down_direction`.
