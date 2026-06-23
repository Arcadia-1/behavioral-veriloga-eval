# Same-Server EVAS/Spectre Speed

Date: 2026-05-26
Claim allowed: `False`
Reason: Same-server timing is measured directly on one host and the artifact emits checker/waveform Spectre-equivalence gates. Paper-facing speed claims should use only equivalence-gated rows and still need repeated cold/warm runs.

## Scope

- Host: `thu-sui`
- Selected rows: 2
- Jobs: 3
- EVAS modes: ``
- Spectre modes: `ax_speed, ax_normalized, reference_strict_primary`
- Output root: `results/settings-normalization-smoke-20260526`

## Mode Summary

| Backend | Mode | Runs | PASS | Non-PASS | Total wall s | Mean wall s |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| spectre | ax_normalized | 2 | 2 | 0 | 1.592 | 0.796 |
| spectre | ax_speed | 2 | 2 | 0 | 1.606 | 0.803 |
| spectre | reference_strict_primary | 2 | 2 | 0 | 6.384 | 3.192 |

## Spectre Run Settings

This table records the final staged testbench settings used by Spectre. For normalized precision-ranking modes, `tran` and `simulatorOptions` are rewritten before Spectre is launched; speed-baseline modes keep the staged testbench unchanged.

| Entry | Form | Variant | Mode | Normalized | CLI args | tran line | simulatorOptions line | Result root |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `ax_speed` | `False` | `+preset=ax +mt` | `tran tran stop=130n maxstep=0.1n` | - | `results/settings-normalization-smoke-20260526/spectre/vbr1_l2_serializer_frame_alignment_flow/e2e/gold/serializer_frame_alignment_smoke/ax_speed` |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `ax_normalized` | `True` | `+preset=ax +mt` | `tran tran stop=130n maxstep=0.1n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/settings-normalization-smoke-20260526/spectre/vbr1_l2_serializer_frame_alignment_flow/e2e/gold/serializer_frame_alignment_smoke/ax_normalized` |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `reference_strict_primary` | `True` | - | `tran tran stop=130n maxstep=0.1n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/settings-normalization-smoke-20260526/spectre/vbr1_l2_serializer_frame_alignment_flow/e2e/gold/serializer_frame_alignment_smoke/reference_strict_primary` |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `ax_speed` | `False` | `+preset=ax +mt` | `tran tran stop=80n maxstep=20p errpreset=conservative` | `simulatorOptions options reltol=1e-4 vabstol=1e-6 iabstol=1e-12 temp=27 tnom=27 gmin=1e-12` | `results/settings-normalization-smoke-20260526/spectre/vbr1_l2_event_controller/e2e/gold/simultaneous_event_order_smoke/ax_speed` |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `ax_normalized` | `True` | `+preset=ax +mt` | `tran tran stop=80n maxstep=20p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 temp=27 tnom=27 gmin=1e-12` | `results/settings-normalization-smoke-20260526/spectre/vbr1_l2_event_controller/e2e/gold/simultaneous_event_order_smoke/ax_normalized` |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `reference_strict_primary` | `True` | - | `tran tran stop=80n maxstep=20p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 temp=27 tnom=27 gmin=1e-12` | `results/settings-normalization-smoke-20260526/spectre/vbr1_l2_event_controller/e2e/gold/simultaneous_event_order_smoke/reference_strict_primary` |

## Spectre-Equivalence Gate Summary

These gates check whether EVAS preserves task behavior and stays within accepted Spectre-equivalent waveform tolerance. They are not a higher-than-Spectre precision target.

| EVAS mode | Runs | Gate PASS | Gate FAIL | Gate BLOCKED | Gate missing |
| --- | ---: | ---: | ---: | ---: | ---: |

## Per-Row Spectre-Equivalence Gates

| Entry | Form | Variant | EVAS mode | Gate | Reasons | Blocked |
| --- | --- | --- | --- | --- | --- | --- |

## Simulation-Only Speedups

| Entry | Form | Variant | Spectre mode | EVAS mode | Spectre wall s | EVAS wall s | Spectre/EVAS |
| --- | --- | --- | --- | --- | ---: | ---: | ---: |

## Spectre-Equivalence-Gated Speedups

| Entry | Form | Variant | Spectre mode | EVAS mode | Spectre wall s | EVAS wall s | Spectre/EVAS |
| --- | --- | --- | --- | --- | ---: | ---: | ---: |

## Interpretation Guardrails

- Speedups use `simulation_ok`, so rows without a behavior checker can still contribute timing if the simulator produced waveforms.
- Equivalence-gated speedups require candidate behavior pass, strict-EVAS parity, and parity to every selected Spectre mode.
- `spectre/ax_speed` is the main fast Spectre speed baseline; `spectre/ax` remains a legacy alias for the same command-line preset.
- `spectre/ax_normalized` keeps `+preset=ax +mt` but rewrites the staged testbench to the shared precision settings before launch.
- `spectre/reference_strict_primary` uses the same staged `tran`/`simulatorOptions` settings without runner-added AX preset.
- `spectre/classic` is the stricter non-X reference path; AX/classic waveform differences are expected and should anchor EVAS tolerance rather than imply a single exact waveform truth.
- The waveform gate is an acceptance tolerance for Spectre-equivalent behavioral output, not a requirement that EVAS exceed Spectre precision.
- Cold Spectre runs include AHDL CMI compilation; warm-cache repetitions should be reported separately.
- A `BLOCKED` gate is not evidence of wrong behavior; it means the checker or reference evidence is incomplete.
