# V4 repair Gate1 batch ledger

- family_count: 10
- class_counts: `{"A": 0, "B": 1, "C": 4, "D": 5}`
- issue: `#279`
- batch: `02/40`
- family_range: `011-020`
- owner: `@BucketSran`
- repair_status: `complete_local_static_and_unit_validation`

| Family | Class | Reasons |
|---|---:|---|
| `011` | `C` | dut: feedback/score body differs<br>dut: feedback/score analysis differs<br>dut: feedback/score parameters differ<br>testbench: feedback/score body differs<br>testbench: feedback/score analysis differs<br>testbench: feedback/score parameters differ<br>testbench: testbench checker has absolute-time/window patterns<br>bugfix: feedback/score body differs<br>bugfix: feedback/score analysis differs<br>bugfix: feedback/score parameters differ |
| `012` | `B` | dut: feedback/score body differs<br>dut: feedback/score analysis differs<br>dut: feedback/score parameters differ<br>testbench: feedback/score body differs<br>testbench: feedback/score analysis differs<br>testbench: feedback/score parameters differ<br>bugfix: feedback/score body differs<br>bugfix: feedback/score analysis differs<br>bugfix: feedback/score parameters differ |
| `013` | `C` | dut: feedback/score body differs<br>dut: feedback/score parameters differ<br>testbench: feedback/score body differs<br>testbench: feedback/score parameters differ<br>testbench: testbench checker has absolute-time/window patterns<br>bugfix: feedback/score body differs<br>bugfix: feedback/score parameters differ |
| `014` | `D` | dut: public trace contract differs from checker observables<br>testbench: public trace contract differs from checker observables<br>bugfix: public trace contract differs from checker observables |
| `015` | `D` | dut: public trace contract differs from checker observables<br>testbench: public trace contract differs from checker observables<br>bugfix: public trace contract differs from checker observables |
| `016` | `C` | dut: feedback/score body differs<br>dut: feedback/score analysis differs<br>dut: feedback/score parameters differ<br>testbench: feedback/score body differs<br>testbench: feedback/score analysis differs<br>testbench: feedback/score parameters differ<br>testbench: testbench checker has absolute-time/window patterns<br>bugfix: feedback/score body differs<br>bugfix: feedback/score analysis differs<br>bugfix: feedback/score parameters differ |
| `017` | `D` | dut: public trace contract differs from checker observables<br>testbench: public trace contract differs from checker observables<br>bugfix: public trace contract differs from checker observables |
| `018` | `D` | dut: public trace contract differs from checker observables<br>testbench: public trace contract differs from checker observables<br>bugfix: public trace contract differs from checker observables |
| `019` | `C` | dut: feedback/score body differs<br>dut: feedback/score analysis differs<br>dut: feedback/score parameters differ<br>testbench: feedback/score body differs<br>testbench: feedback/score analysis differs<br>testbench: feedback/score parameters differ<br>testbench: testbench checker has absolute-time/window patterns<br>bugfix: feedback/score body differs<br>bugfix: feedback/score analysis differs<br>bugfix: feedback/score parameters differ |
| `020` | `D` | dut: public trace contract differs from checker observables<br>testbench: public trace contract differs from checker observables<br>bugfix: public trace contract differs from checker observables |

## Post-repair evidence

- `python3 benchmark-vabench-release-v4/scripts/validate_v4_profile_parity.py --family-range 011-020 --output repair-gate1/issue-279/profile-parity-batch-02.json`: `PASS`, 10 checked, 0 failures.
- `python3 -m pytest tests/test_v4_repair_batch_02.py -q`: `7 passed`.
- `python3 -m pytest tests/test_v4_checker_registry.py -q`: `15 passed`.
- `python3 -m py_compile runners/checkers/v4/trace_utils.py runners/checkers/v4/task_011.py ... runners/checkers/v4/task_020.py benchmark-vabench-release-v4/scripts/validate_v4_profile_parity.py`: `PASS`.
- `git diff --check`: `PASS`.

The repaired checker path is stimulus-relative or observable-event-relative for families `011-020`, feedback and score profiles have zero semantic drift except allowed `simulatorOptions`, checker trace contracts match public observables, and task/denominator hashes were refreshed for the selected range only.

Spectre/Cadence is not available and is not part of this repository's acceptance protocol. Executable validation uses the pinned Rust EVAS2 runtime and records per-case runtime identity.
