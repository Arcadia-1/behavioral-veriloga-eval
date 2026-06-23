# Rust Speed Claim Gate

Date: `2026-06-23`

## Verdict

| Claim | Allowed | Reason |
|---|---:|---|
| `stage55_topwall_engineering_speedup` | `False` | `no_stage_rows`, `stage_completion_below_threshold`, `stage_wall_speedup_not_positive` |
| `full_release_rustification` | `False` | `missing_release_rust_coverage_manifest`, `no_release_models_scanned`, `release_rustification_percent_below_full_threshold` |
| `evas_faster_than_spectre_ax` | `False` | `missing_same_server_ax_artifact` |

## Stage 55 Engineering Gate

- Observed completion: `0.0%`
- Total wall speedup: `None`
- Scope: EVAS-only top-wall engineering slice

## Full Rustification Gate

- Observed release Rustification estimate: `0.0%`
- Threshold for full Rustification claim: `99.9%`
- Behavior blocker count: `0`

## Spectre AX Speed Gate

- EVAS mode: `profile_fast_rust_55`
- Spectre AX mode: `ax_speed`
- EVAS total wall: `None`
- Spectre AX total wall: `None`
- AX/EVAS speedup: `None`

## Next Required Work

- To claim full Rustification: remove all production behavior blockers in the release coverage manifest, not just top-wall fastpaths.
- To claim faster than Spectre AX: run `profile_fast_rust_55` and Spectre AX on the same slice, same server, same settings, with repeated cold/warm runs and equivalence gates.
