# Result Archive Manifest 2026-05-22

Generated raw simulator output was compressed out of the active repository
tree. Keep this manifest as the evidence pointer; restore an archive only when
waveform-level debugging or historical test reproduction needs the raw files.

Archive root:

```text
/Users/bucketsran/Documents/TsingProject/vaEvas/_archives/behavioral-veriloga-eval/raw-results-20260522
```

Restore from the repository root:

```text
tar -xzf /Users/bucketsran/Documents/TsingProject/vaEvas/_archives/behavioral-veriloga-eval/raw-results-20260522/<archive>.tar.gz -C results
```

## Archived Result Roots

| Original result root | Original size | Archive | Archive size | SHA-256 | Summary |
| --- | ---: | --- | ---: | --- | --- |
| `results/vabench-release-v1-dual-rerun-20260516-full-after-fixes` | 290860 KB | `vabench-release-v1-dual-rerun-20260516-full-after-fixes.tar.gz` | 25068635 bytes | `18c8586dff8e8c445304f356dd90779482f01b08595aac757bf45f91150f3f94` | complete dual rerun; `tasks_total=164`, `pass_count=164`, `nonpass_count=0` |
| `results/vabench-release-v1-nonreview-dual-20260518-023558` | 288712 KB | `vabench-release-v1-nonreview-dual-20260518-023558.tar.gz` | 24741068 bytes | `5eca397d4ea89566abfcad75a453d529b05255feabd797bd3bc64c4844940f84` | complete non-review dual rerun; `tasks_total=146`, `pass_count=146`, `nonpass_count=0` |
| `results/vabench-main-v1-main120-gold-evas-2026-05-08` | 16792 KB | `vabench-main-v1-main120-gold-evas-2026-05-08.tar.gz` | 1788505 bytes | `a9c01b03e26c0506f66e882ccec970f120a3d958c2545a97d3563c84826b90b9` | main120 gold EVAS evidence; `total_tasks=120`, `pass_count=120`, `pass_at_1=1.0` |
| `results/vabench-main-v1-main120-gold-spectre-jin-2026-05-08` | 47252 KB | `vabench-main-v1-main120-gold-spectre-jin-2026-05-08.tar.gz` | 5114039 bytes | `bb013d51da81cf5dc5234bb5883f81279fcd6ecc1079c6c79e50464abf623184` | main120 gold Spectre evidence; `total_tasks=120`, `pass_count=120`, `pass_at_1=1.0` |

## References

These archives preserve historical paths referenced by older docs, metadata, or
tests, including:

- `docs/VABENCH_MAIN120_MATERIALIZATION.csv`
- `docs/VABENCH_MAIN120_MATERIALIZATION.md`
- `benchmark-vabench-release-v1/tasks/**/meta.json`
- `benchmark-vabench-release-v1/conformance/**/meta.json`
- `tests/test_p1_checker_hardening.py`

The active workflow should use compact reports and promoted fixtures. Do not
restore these raw results into `results/` unless a reproduction or waveform
debugging task explicitly requires them.

## Validation

Each archive was checked with `tar -tzf <archive>`.
