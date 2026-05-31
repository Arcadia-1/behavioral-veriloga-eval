# Failure Taxonomy Draft (2-Axis) — for Review

Date: `2026-05-26`
Status: **DRAFT — needs human review before adopting**
Source data:
- `datasets/failure_sets/H_ON_F_STABLE_2026-04-26/failures.csv` (33 failures, post-EVAS-repair, condition H-on-F)
- `tables/TABLE2_FAILURE_ANALYSIS.md` (earlier-stage failures: generic-retry + evas-guided-repair)
- `tables/A_FAILURE_REPAIR_ANALYSIS_2026-04-25.md` (existing 8-category sub-taxonomy)

Purpose: replace the current circuit-symptom-based 8-category sub-taxonomy with a circuit-agnostic 2-axis scheme so the classification stays stable as new circuits are added.

---

## 1. Proposed 2-Axis Scheme

### Axis 1 — Pipeline Stage (where the failure manifests)

Reuses existing `FAIL_*` status codes. **Stable across any circuit.**

| Code | Name | Definition | Existing mapping |
|---|---|---|---|
| `S0` | NON_ISSUE | Scoring contract / axis alias problem; not a real failure | `scoring_axis_alias` |
| `S1` | COMPILE | DUT (.va) fails OpenVAF / Spectre compile | `FAIL_DUT_COMPILE` |
| `S2` | SETUP | TB compile fails, missing artifacts, runner infra error | `FAIL_TB_COMPILE`, parts of `FAIL_INFRA` |
| `S3` | EXECUTE | Simulator launches but hangs, NaN, missing CSV, checker timeout | `checker_timeout`, `csv_missing_or_runtime` |
| `S4` | CORRECTNESS | Sim runs to completion, output present, but behavior wrong | most `FAIL_SIM_CORRECTNESS` |

### Axis 2 — Error Mechanism (root cause, abstracted from circuit type)

Designed to be **independent of circuit type**. Adding ADC / PLL / Filter cases should not require new mechanisms.

| Code | Name | Definition | Examples |
|---|---|---|---|
| `M1` | LANGUAGE_CONFUSION | LLM mixes Verilog / Verilog-A / Spectre netlist syntax | `reg`/`wire` in .va; module instantiation in Verilog-A style for Spectre TB |
| `M2` | TOOL_UNSUPPORTED | Construct LLM emits is not supported by the chosen toolchain | OpenVAF rejects `idtmod`; Spectre rejects `laplace_*` |
| `M3` | NUMERICAL_INSTABILITY | Math correct in principle, but causes solver to hang / NaN / non-converge | div by 0, unsmoothed branches, log(<0), step too small |
| `M4` | STRUCTURAL_INCORRECT | Code structure violates Verilog-A scoping / declaration rules; missing artifacts | variable declared inside event block; missing TB file; wrong port direction |
| `M5` | BEHAVIORAL_WRONG | Compiles + runs + outputs, but the modeled behavior is wrong | PLL doesn't lock; ADC outputs constant; counter doesn't toggle |
| `M6` | QUANTITATIVE_DRIFT | Behavior qualitatively correct but numerics off (gain, threshold, bandwidth) | trend right but 30% gain mismatch; threshold offset |

### Reporting axis (orthogonal, not part of the 2D grid)

- **`fix_path`**: prompt-only / KB-rule / runner-policy / out-of-scope (where the fix lives)
- **`fix_difficulty`**: trivial / requires-feedback-loop / requires-architectural-change

---

## 2. Decision Rules (how to assign labels)

Given a failure case, walk this decision tree:

```
1. Did Spectre/OpenVAF reject the .va before sim started?
   YES → S1
        ├─ Mixed Verilog/Spectre syntax (reg, instance order)         → M1
        ├─ Construct not in OpenVAF/Spectre's supported subset        → M2
        └─ Variable scope / declaration / port shape rules            → M4
   NO  ↓

2. Did the runner / TB fail before simulator even launched?
   YES → S2
        ├─ TB syntax / linker issue                                   → M1 or M2
        └─ Missing generated files, harness setup wrong               → M4

3. Did simulator launch but never produce tran.csv / timed out?
   YES → S3
        ├─ Numerical (divergence, NaN, infinite step)                 → M3
        ├─ Code structurally legal but pathological loop / hang       → M3
        └─ Sim ran but harness crashed reading output                 → M4

4. Sim completed, output present, but behavior wrong?
   YES → S4
        ├─ Qualitatively wrong (no edges, no codes, never settles)    → M5
        └─ Qualitatively right but numbers off (gain, threshold)      → M6

5. Status `PASS` but flagged by audit (alias / contract)?
        → S0  (not a real failure; track separately)
```

---

## 3. Re-labeled Dataset (H_ON_F_STABLE_2026-04-26, 33 cases)

| # | Task | Old status | Old mechanism_family | **Stage** | **Mech** | Signature | Confidence | Note |
|---:|---|---|---|---|---|---|---|---|
| 1 | `adc_dac_ideal_4b_smoke` | FAIL_SIM_CORRECTNESS | adc_dac_code_or_output_coverage | **S4** | **M5** | unique_codes=1 vout_span=0 | high | ADC produces no code transitions |
| 2 | `adpll_lock_smoke` | FAIL_SIM_CORRECTNESS | pll_clock_ratio_lock | **S4** | **M5** | not_enough_edges ref=250 fb=0 | high | Feedback path silent |
| 3 | `adpll_ratio_hop_smoke` | FAIL_SIM_CORRECTNESS | pll_clock_ratio_lock | **S4** | **M5** | pre_lock=1.0 post_lock=0.0 | high | Loop loses lock after step |
| 4 | `adpll_timer_smoke` | FAIL_SIM_CORRECTNESS | pll_clock_ratio_lock | **S4** | **M5** | not_enough_edges ref=250 fb=0 | high | Same as #2 |
| 5 | `bad_bus_output_loop` | FAIL_SIM_CORRECTNESS | checker_timeout | **S3** | **M3** | behavior_eval_timeout>53s | medium | Could also be M5 (pathological output); needs probe |
| 6 | `bbpd_data_edge_alignment_smoke` | FAIL_SIM_CORRECTNESS | missing_data_or_reset_window | **S4** | **M5** | too_few_data_edges=0 | medium | Ambiguous: TB stim or DUT? Inspect to confirm |
| 7 | `bg_cal` | FAIL_SIM_CORRECTNESS | adc_dac_code_or_output_coverage | **S4** | **M5** | code_span=15 settled_high=False | high | Bias generator never settles |
| 8 | `cdac_cal` | FAIL_SIM_CORRECTNESS | adc_dac_code_or_output_coverage | **S4** | **M5** | no vdac activity | high | CDAC produces no output |
| 9 | `cppll_freq_step_reacquire_smoke` | FAIL_SIM_CORRECTNESS | pll_clock_ratio_lock | **S4** | **M5** | freq_ratio=0.49 vctrl stuck | high | PLL fails to relock |
| 10 | `cppll_timer` | FAIL_SIM_CORRECTNESS | pll_clock_ratio_lock | **S4** | **M5** | freq_ratio=0.15 lock_time=nan | high | PLL behavior wrong |
| 11 | `cppll_tracking_smoke` | FAIL_SIM_CORRECTNESS | pll_clock_ratio_lock | **S4** | **M5** | freq_ratio=0.40 vctrl stuck | high | Same family |
| 12 | `cross_sine_precision_smoke` | FAIL_SIM_CORRECTNESS | analog_event_crossing | **S4** | **M5** | count_out_too_low=0 | high | `@(cross())` never fires |
| 13 | `dac_therm_16b_smoke` | FAIL_SIM_CORRECTNESS | adc_dac_code_or_output_coverage | **S4** | **M5** | max_vout=0 | high | DAC output stuck at 0 |
| 14 | `digital_basics_smoke` | FAIL_SIM_CORRECTNESS | checker_timeout | **S3** | **M3** | behavior_eval_timeout>53s | medium | Likely numerical hang; inspect tran log |
| 15 | `dwa_ptr_gen_no_overlap_smoke` | FAIL_SIM_CORRECTNESS | checker_timeout | **S3** | **M3** | behavior_eval_timeout>53s | medium | Same |
| 16 | `dwa_ptr_gen_smoke` | **FAIL_INFRA** | missing_generated_testbench | **S2** | **M4** | missing_generated_files:testbench.scs | high | Setup-stage missing file |
| 17 | `dwa_wraparound_smoke` | FAIL_SIM_CORRECTNESS | missing_data_or_reset_window | **S4** | **M5** | insufficient_post_reset_samples=0 | medium | Reset never releases? |
| 18 | `final_step_file_metric_smoke` | FAIL_SIM_CORRECTNESS | checker_timeout | **S3** | **M3** | behavior_eval_timeout>53s | medium | Hang |
| 19 | `flash_adc_3b_smoke` | FAIL_SIM_CORRECTNESS | missing_clock_or_edge_stimulus | **S4** | **M5** | too_few_edges=0 | medium | TB or DUT; needs probe |
| 20 | `gain_extraction_smoke` | FAIL_SIM_CORRECTNESS | checker_timeout | **S3** | **M3** | behavior_eval_timeout>53s | medium | Hang |
| 21 | `gray_counter_one_bit_change_smoke` | FAIL_SIM_CORRECTNESS | missing_clock_or_edge_stimulus | **S4** | **M5** | not_enough_clk_edges=0 | high | Counter doesn't toggle |
| 22 | `multimod_divider_ratio_switch_smoke` | FAIL_SIM_CORRECTNESS | checker_timeout | **S3** | **M3** | behavior_eval_timeout>53s | medium | Hang |
| 23 | `multitone` | FAIL_SIM_CORRECTNESS | csv_missing_or_runtime | **S3** | **M3** | tran.csv missing | high | Sim crashed mid-run |
| 24 | `nrz_prbs` | FAIL_SIM_CORRECTNESS | sequence_frame_or_pulse_generation | **S4** | **M5** | transitions=0 | high | PRBS produces no output |
| 25 | `parameter_type_override_smoke` | FAIL_SIM_CORRECTNESS | sequence_frame_or_pulse_generation | **S4** | **M5** | pulses=0 peak=0 | high | Pulses missing |
| 26 | `pfd_deadzone_smoke` | FAIL_SIM_CORRECTNESS | checker_timeout | **S3** | **M3** | behavior_eval_timeout>53s | medium | Hang |
| 27 | `pfd_reset_race_smoke` | FAIL_SIM_CORRECTNESS | checker_timeout | **S3** | **M3** | behavior_eval_timeout>53s | medium | Hang |
| 28 | `sar_adc_dac_weighted_8b_smoke` | FAIL_SIM_CORRECTNESS | checker_timeout | **S3** | **M3** | behavior_eval_timeout>53s | medium | Hang |
| 29 | `sar_logic_10b` | PASS | scoring_axis_alias | **S0** | — | status_PASS_but_axis_alias | high | Drop from main analysis |
| 30 | `segmented_dac` | FAIL_SIM_CORRECTNESS | adc_dac_code_or_output_coverage | **S4** | **M5** | diff_range=0 | high | DAC output flat |
| 31 | `serializer_frame_alignment_smoke` | FAIL_SIM_CORRECTNESS | sequence_frame_or_pulse_generation | **S4** | **M5** | clk_edges=13 (too few) | medium | Frame timing wrong |
| 32 | `spectre_port_discipline` | PASS | scoring_axis_alias | **S0** | — | axis_alias | high | Drop |
| 33 | `timer_absolute_grid_smoke` | FAIL_SIM_CORRECTNESS | missing_clock_or_edge_stimulus | **S4** | **M5** | too_few_rising_edges=0 | high | Timer behavior wrong |

**Confidence legend**:
- `high`: signature alone is sufficient to assign
- `medium`: ambiguous between two cells; should inspect `.va`/log to confirm before publishing

---

## 4. Heatmap (Stage × Mechanism)

Excluding 2 S0 cases (scoring bugs), n = 31:

```
              M1     M2     M3     M4     M5     M6   | row
S1 COMPILE     0      0      0      0      0      0   |  0
S2 SETUP       0      0      0      1      0      0   |  1
S3 EXECUTE     0      0     10      0      0      0   | 10
S4 CORRECT     0      0      0      0     20      0   | 20
            ----------------------------------------
col            0      0     10      1     20      0      31

Density:
S4 × M5 = 20/31 = 65%   ← behavioral correctness (main residual)
S3 × M3 = 10/31 = 32%   ← sim hangs / numerical instability
S2 × M4 =  1/31 =  3%   ← single missing-TB infra issue
```

**Note on emptiness of S1**: this set is **post-EVAS-repair**, so compile-time errors have been largely eliminated. The pre-repair Table 2 data shows the opposite distribution (compile-stage dominant). See §5.

---

## 5. Cross-Run Distribution Shift (key finding)

Comparing two snapshots from your past runs:

| Snapshot | Stage | Dominant cell | Top mechanism |
|---|---|---|---|
| **Pre-repair** (Table 2 generic-retry) | early | `S1 × (M1+M2+M4)` | language confusion, unsupported syntax, scoping |
| **Post-repair** (H_ON_F_STABLE) | late | `S4 × M5` | behavioral correctness |

**Implication for the paper / benchmark**:

> *EVAS repair has largely solved the compile-stage failures (M1, M2, M4). The remaining failures are concentrated in two cells: (S4, M5) "behavior wrong" and (S3, M3) "simulator hangs". These are the two real research frontiers.*

This is a much sharper finding than "Pass@1 went from 0.29 to 0.58". It tells the reader **what is and isn't solved**, and **where to push next**.

---

## 6. Mechanism Coverage Sanity Check (against Table 2's earlier root causes)

| Table 2 root cause | New label | Covered? |
|---|---|---|
| 根因 1: Verilog-A vs Spectre instantiation syntax confusion | `S1 × M1` | ✓ |
| 根因 2: `reg`/`wire` in Verilog-A | `S1 × M1` | ✓ |
| 根因 3: variable declared inside event block | `S1 × M4` | ✓ |
| 根因 4: dynamic index on signal vector / conditional `transition()` | `S1 × M2` | ✓ (OpenVAF/Spectre constraint) |
| 根因 5: EVAS repair feedback incomplete | not a model error — runner-side bug | — (out of taxonomy scope) |
| 根因 6: repair skill rules incomplete | not a model error — fix-path issue | — (out of taxonomy scope) |

All six existing root causes fit cleanly into the new scheme; 根因 5/6 are correctly identified as **fix-path issues** rather than failure mechanisms.

---

## 7. What I'd Like You to Review

Please flag any of the following:

1. **Cell assignments** — especially the `medium`-confidence rows (5, 6, 14, 15, 17, 18, 19, 20, 22, 26, 27, 28, 31). Some of these may belong in a different cell after looking at the actual `.va` / log.

2. **M3 vs M5 boundary for "checker_timeout"** — I labeled all 9 checker timeouts as `S3 × M3` assuming sim numerically hung. But it's plausible some are actually `S4 × M5` (sim completed quickly but produced pathological output that the checker can't evaluate). Recommend probing 2-3 of these before adopting.

3. **The S2 / S4 ambiguity on "missing_data_or_reset_window"** — cases 6 and 17. Is the missing stimulus a TB-side issue (S2) or a DUT-side reset issue (S4)? Depends on the actual code.

4. **Whether to keep M6 at all** — in this dataset zero cases land in M6 (quantitative drift). Possibly because the benchmark's checkers are gating on coarse behavior, not quantitative thresholds. If you want M6 to be meaningful, the checkers need quantitative metrics (RMSE, gain accuracy, etc.).

5. **Whether the 4 high-level fix-path tags** (`prompt-only`, `KB-rule`, `runner-policy`, `out-of-scope`) should be a third axis or kept as freeform notes.

---

## 8. Proposed Next Steps (if you accept this draft)

1. Apply the same (Stage, Mechanism) labels to the **earlier** failure sets (generic-retry, evas-guided-repair pre-Table-2) so you have a 2-point time series showing the distribution shift.
2. Re-run condition F with a **current 2026-Q2 model** (Claude 4.x or DeepSeek-V4 or GPT-5.5) and re-classify; this gives a third data point — and a publishable "evolution of Verilog-A LLM failures" figure.
3. Promote the (Stage, Mechanism) columns into the canonical `failures.csv` schema. Drop / archive the current circuit-type-specific `mechanism_family` strings, or relegate them to a `sub_tag` column.
4. Write the scoring spec (YAML) — I have a sketch ready; will produce when you sign off on the taxonomy.

---

## Appendix A: Why this taxonomy (vs. the alternatives we considered)

- **vs. 8 categories (PLL / event / divider / ...)**: those are *symptoms by circuit type*, not error mechanisms. Adding a new circuit class would force you to add new categories indefinitely.
- **vs. 7-layer flat structure**: too many layers, several were non-orthogonal (L0/L1 redundant, L5/L6 belong to a different axis).
- **vs. just the existing `FAIL_*` status codes**: too coarse — everything important lives inside `FAIL_SIM_CORRECTNESS`. The Mechanism axis breaks that open.
- **2-axis comes from DeepFix / BugsInPy / SE bug taxonomies**: established practice in code-error classification. VerilogEval/RTLLM use only stage; AnalogCoder mixes both informally. 2-axis is the strict generalization.
