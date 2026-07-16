# V4 repair Gate1 batch ledger

- issue: `#282`
- batch: `05/40`
- family_count: 10
- class_counts: `{"A": 0, "B": 0, "C": 10, "D": 0}`
- repair_status: `complete`
- evas_engine_used: `evas2`
- evas_backend_source: `EVAS 0.4.3`, commit `985bba40929da8066dc9f1e4a08d27c010424c5f`
- batch_evidence: `repair-gate1/issue-282/batch-05-evidence.json`
- evas2_smoke: `repair-gate1/issue-282/evas2-provenance-smoke-041-050.json`
- profile_parity: `repair-gate1/issue-282/profile-parity-041-050.json`
- python_fallback_evidence_claimed: `false`
- not_tested: Cadence/Spectre transient parity; `command -v spectre` found no local executable.

| Family | Class | Result |
|---|---:|---|
| `041` | `C` | Stimulus-relative checker and unified feedback/score semantics pass EVAS2 gold plus five active mutations. |
| `042` | `C` | Sample/droop/reset checker and unified feedback/score semantics pass EVAS2 gold plus five active mutations. |
| `043` | `C` | Hysteresis checker uses stable state metrics and passes EVAS2 gold plus five active mutations. |
| `044` | `C` | Calibration search checker uses observed events and passes EVAS2 gold plus five active mutations. |
| `045` | `C` | Differential comparator checker passes EVAS2 gold plus five active mutations. |
| `046` | `C` | UVLO checker uses observed threshold/latch regions and passes EVAS2 gold plus five active mutations. |
| `047` | `C` | Window comparator checker uses sampled public-window behavior and passes EVAS2 gold plus five active mutations. |
| `048` | `C` | Wide decoder checker uses stable vector rows and passes EVAS2 gold plus five active mutations. |
| `049` | `C` | Wide encoder checker uses stable vector rows and passes EVAS2 gold plus five active mutations. |
| `050` | `C` | ADC checker samples every stable plateau, including clamp endpoints, and passes EVAS2 gold plus five active mutations. |
