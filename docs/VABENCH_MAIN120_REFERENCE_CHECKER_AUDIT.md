# vaBench Main120 Reference-Checker Audit

Date: 2026-05-13

Scope: `vabench-main-v1-main120` local gold evidence:

- EVAS: `results/vabench-main-v1-main120-gold-evas-2026-05-08`
- Spectre: `results/vabench-main-v1-main120-gold-spectre-jin-2026-05-08`

Question: does main120 already have validated reference answers and checker
evidence paired task-by-task?

## Conclusion

Yes. At the result-evidence level, main120 has a complete reference/checker
pairing:

| Check | Result |
| --- | --- |
| Task rows | 120 |
| Base circuit groups | 30 |
| Forms per base | `dut`, `tb`, `bugfix`, `e2e` for every base |
| EVAS PASS | 120/120 |
| Spectre PASS | 120/120 |
| Required axes | `dut_compile=1.0`, `tb_compile=1.0`, `sim_correct=1.0` for all rows on both backends |
| Non-empty `checker_result` | 120/120 on EVAS, 120/120 on Spectre |
| `checker_result.pass` and score | all `pass=true`, `score=1.0` |
| EVAS/Spectre staged `.va`/`.scs` hashes | 120/120 exact matches |
| Missing staged artifact paths / waveform CSVs | none found |

So the current issue is **not** "we lack reference answers or checker evidence."
The current issue is that this evidence is still stored as local validation
results, not yet as reviewed source benchmark tasks with `prompt.md`,
`meta.json`, `checks.yaml`, and checked-in gold files.

## Important Caveats

### 1. Checker evidence exists, but not as reviewed `checks.yaml`

Each result JSON has a passing `checker_result`, for example:

```json
"checker_result": {
  "pass": true,
  "score": 1.0,
  "notes": ["first=0.630 mid=0.570 late=0.630"]
}
```

This proves the gold answer matches the active validation checker used in the
run. It does not yet prove that the public benchmark release has a polished,
human-reviewed `checks.yaml` for that task.

### 2. EVAS/Spectre notes are not always text-identical

52 rows have EVAS/Spectre checker note strings that differ numerically, while
both backends pass. These are tolerance-level or sampling-grid differences, not
binary pass/fail mismatches.

Examples:

| Task | EVAS note | Spectre note |
| --- | --- | --- |
| `vbm1_barrel_pointer_window_dut` | `count_range=(1, 2)` | `count_range=(2, 2)` |
| `vbm1_edge_detector_dut` | `pulse_edges=4 high_frac=0.159` | `pulse_edges=4 high_frac=0.141` |
| `vbm1_first_order_lowpass_dut` | `early=0.450 late=0.798` | `early=0.449 late=0.798` |
| `vbm1_leaky_hold_dut` | `high=0.655 decayed=0.265 rst=0.000` | `high=0.659 decayed=0.263 rst=0.000` |
| `vbm1_pfd_reset_race_dut` | `up_first=0.0100 ... overlap_frac=0.0000` | `up_first=0.0101 ... overlap_frac=0.0000` |
| `vbm1_vco_phase_integrator_dut` | `early_edges=2 late_edges=4 phase_span=0.995` | `early_edges=2 late_edges=4 phase_span=0.992` |

Update on 2026-05-14: the VCO row was not merely a checker-tolerance issue.
It was traced to EVAS startup semantics for `timer(0,...)` feeding
`transition()`. After the EVAS initial-condition fix, the staged main120 VCO
DUT rerun gives first `phase=0.039` and `phase_span=0.992`, matching the
Spectre-backed mathematical expectation. When this audit is regenerated, that
row should move from "checker note tolerance" to "resolved EVAS/Spectre
conformance regression".

Recommendation: materialized `checks.yaml` should encode threshold/tolerance
checks, not exact note-string equality.

### 3. Most `bugfix` rows do not preserve the buggy source

All 30 bugfix rows have a passing fixed reference answer and testbench, so they
are valid as reference/checker evidence. However, only one staged bugfix row
currently contains explicit buggy and fixed sources:

- `vbm1_strongarm_comparator_behavior_bugfix`:
  `dut_buggy.va`, `dut_fixed.va`, `tb_strongarm_reset_priority_bug_ref.scs`

The other 29 bugfix rows are staged as fixed-source-only evidence, for example
`pfd_updn.va` plus `tb_pfd_reset_race_ref.scs`.

Recommendation: when materializing these rows, either reconstruct/review the
buggy code in `prompt.md`, or convert the row to a non-bugfix form if no honest
buggy input can be recovered.

### 4. One base intentionally differs across forms

The `strongarm_comparator_behavior` base has form-specific staged files:

- `bugfix`: reset-priority bug task with `dut_buggy.va` / `dut_fixed.va`
- `dut`, `tb`, `e2e`: normal comparator behavior task with `cmp_strongarm.va`

This is not an EVAS/Spectre mismatch; source hashes still match between EVAS
and Spectre per task. It is a reminder that "30 bases x 4 forms" does not always
mean the four forms are byte-identical tasks.

## Materialization Implication

For main120, the next step should be:

1. Treat the staged `.va`/`.scs` files and result JSON checker notes as gold
   evidence.
2. Materialize source task directories from that evidence.
3. Write reviewed `prompt.md` files that describe the intended behavior without
   overclaiming circuit semantics.
4. Convert each checker note pattern into a public `checks.yaml` behavior
   contract with tolerances.
5. For bugfix rows, explicitly add or reconstruct the buggy input source, or
   reclassify the task form.

This keeps the mainline clean: main120 already has validated reference/checker
evidence, but it is not yet a fully release-ready benchmark source split.
