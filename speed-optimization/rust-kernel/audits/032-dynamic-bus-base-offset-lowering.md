# 032 - Dynamic Bus Base/Index Runtime Lowering

Status: `done`

Date: `2026-06-03`

Code commit: `a91570a` (`EVAS`, branch `codex/evas-spectre-rulefix-20260529`)

Related reports:

- `speed-optimization/rust-kernel/audits/019-dynamic-bus-lowering-prototype.md`
- `speed-optimization/rust-kernel/audits/023-dynamic-bus-runtime-codegen-fix.md`
- `speed-optimization/rust-kernel/audits/031-runtime-parameter-affine-lowering.md`

## One-Line Summary

把 generated dynamic bus read/write 从每次直接格式化 `bus[i]` 节点名，改成经过 `_resolve_dynamic_node(base, index, index2)` 的 base/index cache；语义仍是旧的 node-string path，但重复访问不再反复构造同一个字符串。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| Dynamic bus codegen | 生成 `self._format_dynamic_node("dout", i)` | 生成 `self._resolve_dynamic_node("dout", i)` | waveform 不变 |
| Runtime helper | 每次 `int(index)` 后拼字符串 | 按 `(base, int(index), int(index2))` 缓存节点名 | 默认 backend 结果不变 |
| Safety bound | 无缓存增长问题 | 每个 model 最多缓存 `4096` 个 dynamic node key，超过后 bypass | 避免异常大 index 空间无限增长 |
| Observability | 无法量化 dynamic bus hot path | 新增 `dynamic_node_cache_hits/misses/bypasses/entries` counters | 后续 benchmark 可看 bus 路径是否真实命中 |
| Tests | 只检查没有 nested f-string | 增加 cache hit/miss 和 simulator aggregation 测试 | state-index case 保持正确 |

## Principle

这一步属于 **减少每步 Python 字符串构造成本**，不是完整 Rust node-id lowering。

dynamic bus 的原始执行形状是：

```text
for each step:
  for i in bus indices:
    node = "dout[" + str(int(i)) + "]"
    _set_output(node, value, node_voltages)
```

如果 `i` 在每步反复落到同一组小整数，例如 ADC/DAC/DEM 里的 fixed-width bus，那么同一个字符串会被构造很多次。032 改成：

```text
key = (base, int(i), None)
node = dynamic_node_cache[key]
_set_output(node, value, node_voltages)
```

第一次访问 `dout[7]` 会 miss 并创建字符串，之后同一个 index 直接命中 cache。

这仍然保留 `_get_voltage()` / `_set_output()` 的旧语义，所以：

- node map 解析仍由原有路径处理；
- event context 的 interpolation 仍由 `_get_voltage()` 处理；
- 2D bus 仍只是缓存 `base/index/index2 -> string`；
- 没有把 dynamic bus 误接入 static branch direct-array path。

真正的 Rust 化目标会是：

```text
node_id = base_node_id + offset
value = values[node_id]
```

032 只先把 runtime 入口收敛成一个 resolver，并证明简单 bus 场景的重复字符串构造可以被消掉。完整 node-id offset lowering 还需要更严格证明 bus range、index coercion、2D layout 和 event-body read 的边界。

## Before / After Evidence

| Metric | Cache disabled | Cache enabled | Interpretation |
|---|---:|---:|---|
| 16-lane dynamic bus sample median wall | `0.034590708 s` | `0.030722917 s` | local microbench 约 `1.13x` |
| best wall | `0.033717875 s` | `0.030256416 s` | 同一脚本、同一模型 |
| cache hits | `0` | `16032` | 1001 steps 后绝大多数 dynamic node 解析命中 |
| cache misses | `0` | `16` | 16 个 bus lane 各 miss 一次 |
| cache bypasses | `16048` | `0` | disabled path 用 limit=0 模拟不缓存 |
| cache entries | `0` | `16` | 缓存规模等于 bus width |
| steps | `1001` | `1001` | 步数不变，精度/调度不变 |

解读：

- 这不是全局 EVAS speed claim，只说明 dynamic bus 字符串热路径有局部优化价值。
- 对不使用 dynamic bus 的 benchmark，没有直接速度收益。
- 对 bus width 小且每步重复访问的模型，cache 命中率很高。
- 当前仍然要走 `_get_voltage()` / `_set_output()` 和 dict/node_map 路径，所以收益有限。

## Functional Safety

- Default backend changed: `yes, but behavior-preserving helper replacement`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Event ordering changed: `no`
- Rust ABI changed: `no`
- Fallback path exists: `yes, cache bypasses after limit`

## Validation

Commands run:

```bash
python3 -m pytest tests/test_indexed_backend.py::test_compiled_model_counts_dynamic_branch_io_metadata tests/test_indexed_backend.py::test_dynamic_branch_codegen_handles_state_index_expression_without_nested_fstring tests/test_indexed_backend.py::test_simulator_aggregates_dynamic_bus_node_cache_stats tests/test_indexed_backend.py::test_compiled_model_records_dynamic_branch_access_ir_for_2d_reads tests/test_indexed_backend.py::test_indexed_model_io_plan_exposes_dynamic_branch_accesses -q
python3 -m pytest tests/test_indexed_backend.py tests/test_engine.py::Test2DNodeArray::test_1d_array_contribution_compiles tests/test_engine.py::Test2DNodeArray::test_2d_array_contribution_compiles tests/test_engine.py::Test2DNodeArray::test_2d_array_read_voltage -q
python3 -m pytest tests -q
cargo test --release
git diff --check
cargo clean
```

Results:

```text
dynamic bus targeted pytest: 5 passed
indexed/2D wider pytest: 30 passed
full pytest: 465 passed in 57.07s
cargo test --release: 3 passed
git diff --check: clean
```

Microbenchmark:

```text
cache_disabled median 0.034590708 best 0.033717875 hits 0 misses 0 bypasses 16048 entries 0 steps 1001
cache_enabled  median 0.030722917 best 0.030256416 hits 16032 misses 16 bypasses 0 entries 16 steps 1001
```

## Learning Notes

### 为什么 dynamic bus 比普通 node 难？

普通 node 是编译时固定的：

```text
V(vout) <+ ...
```

编译器可以提前知道 node 名是 `vout`，后续可以映射到固定 node id。

dynamic bus 是运行时决定的：

```text
V(dout[ch]) <+ ...
```

这里的 `ch` 可能来自：

- `genvar` loop；
- integer state；
- parameter expression；
- event body 中更新的状态；
- 2D bus 的两个 index。

所以不能简单把所有 `dout[ch]` 都当成一个固定 node。

### 为什么缓存是安全的？

缓存 key 是已经按旧语义转成 integer 的 index：

```text
(base, int(index), int(index2))
```

同一个 key 永远对应同一个字符串节点名，例如：

```text
("dout", 2, None) -> "dout[2]"
```

后续 `_get_voltage()` / `_set_output()` 仍然走原来的 voltage path。也就是说，032 没有改变电压值如何读取、写入、插值或映射，只减少了重复字符串构造。

### 这离 Rust 化还差什么？

Rust 最想要的不是字符串 cache，而是整数下标：

```text
values[node_id]
```

要安全做到这一点，还需要证明：

1. `dout[0]...dout[N]` 的 node id 是稳定且可查的；
2. index coercion 和 Verilog-A integer 规则一致；
3. 2D bus 的内存布局明确；
4. event body 读不会错误地绕过 crossing-time interpolation；
5. dynamic output write 和 subsequent Python model read 不会状态不同步。

032 的作用是把 dynamic bus runtime 先收敛到一个可替换入口，后续可以把 resolver 的返回值从 string 逐步扩展到 node id / offset。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| cache key coercion 改变 index 语义 | state-index dynamic bus test 失败 | revert EVAS commit `a91570a` |
| cache 过大导致内存增长 | `dynamic_node_cache_entries` 接近 `4096` 且 bypass 非零 | 调低 limit 或改为 LRU |
| 被误解为完整 Rust dynamic bus lowering | 报告宣称 bus 已经 `Vec<f64>` offset 访问 | 引用本审计 claim boundary |
| event body read 被误静态化 | event/interpolation waveform mismatch | 032 未改 event read path；若出现问题先回退 codegen helper |

## Next Step

下一篇审计：

- `033-indexed-state-runtime-storage.md`：开始把 scalar/int/array state 从 metadata 推进到 opt-in indexed runtime mirror，为后续 Rust state ABI 做准备。
