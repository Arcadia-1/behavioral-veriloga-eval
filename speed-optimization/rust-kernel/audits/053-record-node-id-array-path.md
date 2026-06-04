# 053 - Record Node-ID Array Path

Status: `done`

Date: `2026-06-04`

Code commit: `pending`

Related documents:

- `049-behavior-coverage-manifest.md`
- `052-cross-above-detector-rust-primitives.md`
- `../behavior-coverage-map.v1.json`

## One-Line Summary

为 B15 record path 增加 indexed node-id 读取切片：`indexed_arrays=True` 时 `_record_point()` 使用预计算 `recorded_node_ids` 从 `IndexedVoltageArray` 批量取值，避免每个记录点重复按 signal name 做 dict/name lookup；`SimResult` 和 CSV schema 不变。

## Why This Exists

速度测试里 CSV/checker/record 属于 E2E 开销，不是核心模型 evaluate。但只要我们做 release-wide timing，record 和 CSV 仍会进入 wall time。B15 的长期目标是：

```text
node/state array -> sparse required-signal trace -> checker/CSV writer
```

这次只完成第一小步：

```text
recorded signal names -> run-start node ids
每个 record point -> 按 id 从 array 读值
```

这样做不会改变输出格式，但把 record path 从“每次用字符串找节点”推进到“每次按整数 id 读数组”，为未来 Rust record batch 准备边界。

## Changed Code

| Area | File | Change |
|---|---|---|
| Indexed helper | `EVAS/evas/simulator/indexed.py` | 新增 `IndexedVoltageArray.values_for_ids()` |
| Engine | `EVAS/evas/simulator/engine.py` | `indexed_arrays=True` 时预计算 `indexed_record_node_ids`，`_record_point()` 走 id-array 读取；新增 `indexed_array_record_id_reads` counter |
| Tests | `EVAS/tests/test_indexed_backend.py` | 验证 batch node-id 读取和 missing id fallback |
| Tests | `EVAS/tests/test_engine.py` | 验证 indexed record waveform 与默认 dict path 一致，并记录 id-read counter |

## Claim Boundary

这不是“B15 已全量 Rust 化”。目前仍然是：

| Piece | Status |
|---|---|
| record value lookup | indexed array/id path in Python |
| Python list append | still Python |
| `SimResult` numpy conversion | still Python/Numpy |
| CSV writer | still Python/Numpy, schema unchanged |
| checker required-signal sparse trace | not implemented |
| Rust record ABI | not implemented |

## Verification

Fresh checks:

```text
PYTHONPATH=EVAS PYTHONPYCACHEPREFIX=/private/tmp/evas-pycache python3 -m pytest EVAS/tests/test_indexed_backend.py::test_indexed_voltage_array_reads_batch_by_node_ids_without_name_lookup -q
1 passed

PYTHONPATH=EVAS PYTHONPYCACHEPREFIX=/private/tmp/evas-pycache python3 -m pytest EVAS/tests/test_engine.py::TestSimulator::test_indexed_arrays_preserve_source_record_and_error_scan_results -q
1 passed

PYTHONPATH=EVAS PYTHONPYCACHEPREFIX=/private/tmp/evas-pycache python3 -m pytest EVAS/tests/test_rust_backend.py -q
16 passed
```

## Next Step

The next B15 step should not change CSV schema yet. A safe follow-up is to store recorded trace columns as preallocated or chunked arrays, then compare memory/time against the current Python list append path before considering sparse/edge trace output.
