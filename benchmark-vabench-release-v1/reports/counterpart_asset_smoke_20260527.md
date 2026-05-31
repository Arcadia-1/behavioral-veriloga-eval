# Counterpart Asset Smoke - 2026-05-27

This is a non-certifying smoke report for the repaired counterpart assets. It checks whether the staged assets are runnable and whether buggy/fixed counterparts exercise the checker as expected. It does not replace full EVAS/Spectre dual certification.

## Scope

Smoke queue:

- `vbr1_l1_dac_mismatch_unit_weighting_model`: `dut`, `tb`, `bugfix`, `e2e`
- `vbr1_l1_higher_order_filter`: `dut`, `tb`, `bugfix`, `e2e`
- `vbr1_l1_charge_pump_abstraction`: `dut`, `tb`, `bugfix`, `e2e`

Artifacts:

- Queue: `benchmark-vabench-release-v1/reports/counterpart_asset_smoke_queue_20260527.json`
- Staging manifest: `benchmark-vabench-release-v1/reports/counterpart_asset_smoke_staging_manifest_20260527.json`
- EVAS-only result: `benchmark-vabench-release-v1/reports/counterpart_asset_smoke_evas_only_20260527.json`
- Dual smoke result: `results/vabench-release-v1-counterpart-smoke-20260527-r1/summary.json`
- One-case Spectre retry: `results/vabench-release-v1-counterpart-smoke-20260527-r2-onecase/summary.json`

## Staging

Command:

```bash
python3 runners/prepare_vabench_release_dual_rerun.py \
  --queue-json benchmark-vabench-release-v1/reports/counterpart_asset_smoke_queue_20260527.json \
  --staging-root benchmark-vabench-release-v1/rerun_staging_counterpart_smoke_20260527 \
  --manifest-json benchmark-vabench-release-v1/reports/counterpart_asset_smoke_staging_manifest_20260527.json \
  --manifest-csv benchmark-vabench-release-v1/reports/counterpart_asset_smoke_staging_manifest_20260527.csv \
  --manifest-md benchmark-vabench-release-v1/reports/counterpart_asset_smoke_staging_manifest_20260527.md
```

Result:

- `15/15` staged bundles ready.
- `12/12` queue rows runnable.
- The extra 3 bundles are buggy companions for the `bugfix` form.

## EVAS-Only Smoke

Result:

- Bundles checked: `15`
- PASS: `12`
- Expected checker failures: `3`
- Expected misses: `0`

Status counts:

| Status | Count |
| --- | ---: |
| `PASS` | 12 |
| `FAIL_SIM_CORRECTNESS` | 3 |

Interpretation:

- All gold/fixed primary bundles passed EVAS.
- All three buggy companions failed EVAS correctness checks, as intended.
- No missing generated file, missing include, missing testbench, or checker-routing failure remains in this smoke slice.

## Spectre Dual Smoke

Command:

```bash
python3 runners/run_vabench_release_dual_rerun.py \
  --manifest benchmark-vabench-release-v1/reports/counterpart_asset_smoke_staging_manifest_20260527.json \
  --output-root results/vabench-release-v1-counterpart-smoke-20260527-r1 \
  --spectre-backend sui-direct \
  --workers 3 \
  --timeout-s 300 \
  --spectre-license-wait-s 120
```

Result:

- Tasks: `12`
- Raw status: `FAIL_SPECTRE` 8, `FAIL_EVAS` 4
- EVAS status before the higher-order-filter fix: `PASS` 8, `FAIL_SIM_CORRECTNESS` 4
- Spectre status: all 12 attempts failed with:
  - `spectre_failed rc=2`
  - `spectre_license_checkout_failed:SPECTRE-209`

One-case retry:

```bash
python3 runners/run_vabench_release_dual_rerun.py \
  --manifest benchmark-vabench-release-v1/reports/counterpart_asset_smoke_staging_manifest_20260527.json \
  --output-root results/vabench-release-v1-counterpart-smoke-20260527-r2-onecase \
  --spectre-backend sui-direct \
  --workers 1 \
  --timeout-s 420 \
  --spectre-license-wait-s 300 \
  --entry vbr1_l1_charge_pump_abstraction \
  --form dut
```

The one-case retry also failed with `SPECTRE-209` after `+lqtimeout 300`, while EVAS passed. This identifies the current Spectre blocker as license checkout unavailability, not asset staging.

## Fix Applied During Smoke

The first dual smoke exposed an EVAS correctness issue in the higher-order-filter gold asset: the checker expects reset output near the 0.45 V common-mode level, but the model initialized and reset the two pole states to 0.0 V.

Fix:

- Initialize/reset `s1`, `s2`, and `y` to `0.45` for the `two_pole_filter` profile.
- Preserve the buggy counterpart's intended fault as the missing lagged second pole update (`s2 = s1`).

Post-fix EVAS smoke confirmed:

- `vbr1_l1_higher_order_filter` `dut`, `tb`, `bugfix/fixed`, and `e2e` pass.
- `vbr1_l1_higher_order_filter` `bugfix/buggy` fails as expected with `two_pole_missing_lagged_rise`.

## Validation

Targeted regression:

```bash
PYTHONPATH=runners PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache python3 -m pytest \
  tests/test_vabench_release_score_runnable_assets.py \
  tests/test_vabench_release_asset_integrity.py \
  tests/test_vabench_release_prompt_contract_manifest.py \
  tests/test_vabench_release_schema_validation.py \
  tests/test_vabench_release_package_manifest.py -q
```

Result: `15 passed in 0.39s`.

## Conclusion

Counterpart asset smoke passes on the EVAS side. The repaired assets are staged correctly, fixed/gold bundles pass, and buggy companions are caught by checkers.

This smoke is not a full EVAS/Spectre certification because Spectre is currently blocked by `SPECTRE-209` license checkout failure on `thu-sui`.
