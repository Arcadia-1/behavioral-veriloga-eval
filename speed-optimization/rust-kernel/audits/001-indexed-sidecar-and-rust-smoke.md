# 001 - Indexed Sidecar And Rust Smoke

Status: `done`

Date: `2026-06-02`

Code commit: `EVAS 37c451a`

Related paths:

- `EVAS/evas/simulator/indexed.py`
- `EVAS/tests/test_indexed_backend.py`
- `EVAS/evas/examples/backend_migration_capability_manifest.json`
- `EVAS/tests/test_backend_migration_capability_manifest.py`
- `EVAS/prototypes/rust-kernel-smoke/`

## One-Line Summary

正式 Rust 化前，先建立 indexed sidecar、Rust toy kernel 和 capability manifest，让后续大改有回退点、性能预期和功能不删减边界。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| node/state mapping | 运行时主要依赖 string/dict | 新增 `NodeIndex`、`StateIndex`、`IndexedVoltages` helper | 默认仿真路径不变 |
| Rust feasibility | 只有 Python kernel 直觉 | 新增 standalone Rust toy benchmark | 不进入默认 EVAS |
| migration coverage | `tests/test_examples.py` 覆盖 11 个 validator TB | manifest 覆盖 16 个 bundled TB | 默认测试不变，迁移门槛更清楚 |
| documentation | Rust wiki 在 EVAS repo | 迁移到 `speed-optimization/rust-kernel/` | 文档归到速度优化主线 |

## Principle

这一步本身不是直接加速默认 EVAS，而是为后续加速铺路：

- indexed helper 把“字符串名字”整理成稳定整数 id，这是 Rust backend 必须消费的数据形态。
- Rust toy kernel 验证 native indexed loop 和 event queue 的潜在收益。
- capability manifest 防止后续为了速度删掉 EVAS 原本能仿真的内容。

## Before / After Evidence

| Metric | Before | After | Interpretation |
|---|---:|---:|---|
| Python measurement dict toy | `16.590893 s` | unchanged | 当前 Python dict 风格热路径的参考 |
| Python measurement indexed toy | none | `9.852070 s` | Python 内 indexed 约 `1.684x`，但仍受解释器限制 |
| Rust measurement indexed toy | none | `0.135588 s` | Rust native indexed toy 比 Python indexed 约 `72.662x` |
| Python PFD fixed-step toy | `0.732351 s` | unchanged | 固定步扫描参考 |
| Python PFD event-queue toy | none | `0.060759 s` | event queue 在 Python toy 中约 `12.053x` |
| Rust PFD event-queue toy | none | `0.000474 s` | native event queue 方向值得继续 |
| bundled example TB in migration manifest | none | `16` | 新 backend 不能少仿原 EVAS examples |

这些数字来自 toy benchmark，只能指导工程方向，不能作为 paper-facing EVAS/AX speed claim。

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`, 因为新结构目前只是 sidecar/prototype

## Validation

Commands run:

```bash
python3 -m pytest tests -q
cargo test --release
git diff --cached --check
PYTHONPYCACHEPREFIX=/private/tmp/evas-checkpoint-pycache python3 -m py_compile ...
```

Results:

```text
410 passed in 22.38s
2 Rust tests passed
```

## Learning Notes

### 什么是 sidecar？

sidecar 是“放在旁边的辅助结构”。这次的 indexed helper 没有替换原仿真器，只是提供新 backend 未来会用到的数据结构。好处是风险低：如果 helper 有问题，不会影响默认仿真。

### 什么是 node id？

原来仿真器用节点名读电压：

```python
node_voltages["vin"]
```

node id 是先把名字编号：

```text
vin -> 0
vout -> 1
clk -> 2
```

之后热循环只读数组：

```rust
curr[vin_id]
```

### 为什么 toy benchmark 不能当最终结论？

toy benchmark 只保留了内核瓶颈的形状，排除了真实 Verilog-A 语义、netlist hierarchy、checker、CSV、Spectre parity 等复杂因素。它能回答“方向是否值得继续”，不能回答“真实 release 上 EVAS 是否比 AX 更快”。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| 新 backend 后续误用 indexed helper 改变节点 alias | examples manifest 或 parity test 失败 | 回退到 Python dict backend |
| Rust toy 数字被误当 paper claim | 报告中出现 release-wide claim 但没有 same-slice artifact | 只引用 release speed artifact |
| 文档分散导致找不到顺序 | 后续审计没有编号 | 回到 `rust-kernel/README.md` 维护时间线 |

## Next Step

下一篇审计文档建议：

- `002-python-indexed-ir-parity.md`：建立 opt-in Python indexed IR/parity harness，先证明“名字到编号”的 lowering 不改变行为。
