# 096 - `rust_transition_production` Net-Negative On Real Release

Status: `done` (recommend downgrading the flag)

Date: `2026-06-06`

Code commit: `pending`

Related documents:

- `086-transition-output-rust-handoff.md`
- `088-transition-output-per-step-batch.md`
- `097-cmp-strongarm-rust-slowdown-root-cause.md`

## One-Line Summary

Audit 086/088 reported `rust_transition_production` as "+2.8% real" based on one transition-heavy synthetic bench. The 80-row real-release sweep here shows the flag is net negative on **74/75** measured rows (zero wins, geomean **0.56×**, total wall **81.8s → 152.3s**, **+86%**), confirming the cmp_strongarm regression in audit 097 is the rule, not the exception. Recommend dropping the flag from "default-on candidate" to "experimental, off by default".

## Why This Sweep Exists

Audit 086 introduced a Rust path for `_flush_transitions`; audit 088 wrapped it with per-step batching and claimed "+2.8%". Both numbers came from a single transition-heavy stress bench. Audit 097 then found cmp_strongarm runs ~2× slower with the flag on. Before changing engine defaults we needed to settle one question:

> **Across the entire real release**, is `rust_transition_production=True` a win, a wash, or a loss?

This sweep answers that with measured wall time across every tb-form row whose 091b matcher reports `transition_target_ir` (i.e., rows where the Rust path is supposed to help).

## Setup

| Knob | Value |
|---|---|
| Manifest | `current_release_rust_coverage_manifest_20260604.json` |
| Row filter | `form == "tb"` AND `"transition_target_ir" ∈ rust_signals` AND dedup by `sha256` |
| Candidate count | 80 |
| Repeats / row | 3 (median taken) |
| Modes / row | Python default vs `rust_required=True, rust_transition_production=True` |
| Deadline / run | 30 s (marked SKIP if exceeded) |
| Runner | `EVAS/prototypes/audit_096_transition_production_sweep.py` |
| Raw results | `EVAS/prototypes/audit_096_sweep_results.json` |

## Aggregate

| Metric | Value |
|---|---|
| Measured rows | 75 / 80 (5 timed out and were skipped) |
| Speedup range | **0.24× .. 0.99×** |
| Speedup median | **0.58×** |
| Speedup geomean | **0.56×** |
| Wins (>1.05×) | **0** |
| Neutral (0.95-1.05×) | 1 (`ldo_regulator_macro_model` 0.99×) |
| Losses (<0.95×) | 74 |
| Big losses (<0.5×) | 14 |
| Python total wall | 81.81 s |
| Rust total wall | 152.31 s |
| Overall ratio | **0.54×** (rust is ~86% slower) |

## Worst 10 Rows

| Row | py wall | rust wall | speedup |
|---|---:|---:|---:|
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | 0.632 s | 2.645 s | **0.24×** |
| `vbr1_l1_bias_voltage_generator_with_enable_trim` | 0.076 s | 0.294 s | **0.26×** |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | 1.037 s | 3.149 s | **0.33×** |
| `vbr1_l1_power_on_reset_detector` | 0.085 s | 0.253 s | **0.34×** |
| `vbr1_l1_gain_trim_controller` | 0.651 s | 1.799 s | **0.36×** |
| `vbr1_l1_pa_compression_macro` | 0.077 s | 0.208 s | **0.37×** |
| `vbr1_l1_edge_interval_timer` | 5.930 s | 14.597 s | **0.41×** |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | 6.719 s | 14.912 s | **0.45×** |
| `vbr1_l1_slew_rate_limiter` | 0.042 s | 0.092 s | **0.46×** |
| `vbr1_l1_resettable_integrator` | 0.127 s | 0.272 s | **0.47×** |

The two heaviest absolute losses on the list (`edge_interval_timer` +8.7 s, `capacitive_weighted_sar_feedback_dac` +8.2 s) together explain ~24% of the total wall regression.

## Best Row Is Still A Loss

`vbr1_l1_ldo_regulator_macro_model` at 0.99× is the closest to break-even and is still a (tiny) loss. There is **no row in the 75-row measured set** where this flag pays off.

## Why The Flag Loses

The per-step batching from audit 088 reduces the number of flushes versus 086, but does not change the basic accounting:

| Component | Per-event cost |
|---|---|
| ctypes FFI round-trip into Rust | ~20–25 µs |
| Python `_flush_transitions` implementation | ~3–6 µs of arithmetic on small lists |

Real release rows do not have transition densities anywhere close to the synthetic bench. They have many simulator steps each carrying a small handful of transitions, so flushes happen often but with little work per flush. The FFI overhead is paid every time; the savings inside Rust are not enough to repay it. This is the same pathology that 097 identified on cmp_strongarm — the sweep here shows the pathology is universal across the release, not a single outlier.

## Recommendation

1. Demote `rust_transition_production` from "default-on candidate" to **experimental, off by default**. Mark it in the gate inspector output as a known regression on real workloads.
2. The audit 086/088 "+2.8% real" claim should be **scoped to the original transition-heavy bench only** — it does not generalize. Update the rust-kernel README accordingly.
3. Do **not** wire this flag into Stage 5 (paper-facing Spectre rerun). Use the 091d generic executor path instead, where audit 093 showed real wins.
4. Any future revisit of Rust-side transition acceleration must batch across **multiple simulator steps**, not just within one step — single-step batch is provably insufficient to amortize FFI on real rows.

## What This Sweep Does NOT Cover

- `rust_event_detector` / `rust_segment_executor` flags — out of scope; this audit only isolates `rust_transition_production`.
- The 091d generic event-state-transition fastpath — that path was already validated in 093/095 and is unaffected.
- Bit-exact CSV parity — this sweep measured wall time only. Parity for this flag was checked separately in audit 086.

## Claim Boundary

**Can say:**

- `rust_transition_production=True` is net negative on real release workloads (0 wins out of 75).
- The 086/088 "+2.8%" number is not representative of release behavior.
- Per-step FFI batching is not enough to make a Rust transition writer pay off.

**Cannot say:**

- A *cross-step* Rust transition writer would also lose. (Untested.)
- The flag should be deleted from the codebase. It is still useful for the original transition-heavy bench and for future cross-step experiments — demote, do not remove.

## Reproduce

```bash
cd EVAS
PYTHONPATH=. python3 prototypes/audit_096_transition_production_sweep.py
# ~16 minutes wall; writes prototypes/audit_096_sweep_results.json
```
