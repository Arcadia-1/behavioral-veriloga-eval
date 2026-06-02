# 020 - Indexed Model State Arrays

Status: `done`

Date: `2026-06-03`

Code commit: `EVAS 708ebf7`

Related paths:

- `EVAS/evas/simulator/backend.py`
- `EVAS/evas/simulator/indexed.py`
- `EVAS/evas/simulator/engine.py`
- `EVAS/tests/test_indexed_backend.py`
- `EVAS/tests/test_netlist.py`

## One-Line Summary

为 model-local scalar state 和 array state 建立 indexed layout metadata，让未来 Rust model-evaluate ABI 可以接收稳定 state id 和 array range；当前不替换 Python `self.state` / `self.arrays`。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| compiled model metadata | state 只在 generated `__init__` 中写入 `self.state` / `self.arrays` | 新增 `_state_scalar_names`、`_integer_state_names`、`_state_array_ranges` | 默认仿真不变 |
| indexed model IO plan | 只描述 node IO、dynamic bus、event/static read/write | 新增 per-model `state_scalar_names`、`state_scalar_ids`、`integer_state_names`、`state_array_layouts` | 只影响 opt-in IR/stats |
| simulator stats | 不显示 model state layout 汇总 | 新增 scalar/integer/array state count 和 array slot count | 只影响日志诊断 |
| runtime state storage | Python dict: `self.state["x"]`、`self.arrays["a"][i]` | 完全不改 | state behavior 不变 |

## Principle

这个改动是 **Rust 化前置 IR**，目标是把 Python object-heavy state 访问变成未来可替换的数据结构。

现在 EVAS 的 model state 类似：

```python
self.state["code"]
self.state["sample"]
self.arrays["bins"][i]
```

这对 Python 来说方便，但在热循环里会带来：

- 字符串 key lookup；
- dict object indirection；
- integer/real coercion 分散在 generated code 中；
- array state 是 dict-of-dict，不是连续内存。

未来 Rust 更自然的形式是：

```text
scalar_state[0] = x
scalar_state[1] = code
array_state[bins_base + i] = value
```

020 先不改执行，只把 state layout 显式化：

```text
_state_scalar_names = ("x", "code", "i")
_integer_state_names = ("code", "i")
_state_array_ranges = (("accum", 0, 3, False), ("bins", 0, 2, True))
```

indexed plan 再给 scalar state 分配 per-model id：

```text
state_scalar_names = ("x", "code", "i")
state_scalar_ids   = (0, 1, 2)
```

这一步让 021 的 Rust ABI prototype 可以明确 state 输入/输出布局。

## Before / After Evidence

Validation commands:

```bash
python3 -m pytest tests/test_indexed_backend.py::test_compiled_model_records_state_layout_metadata tests/test_indexed_backend.py::test_indexed_model_io_plan_exposes_state_layouts -q
python3 -m pytest tests/test_netlist.py::TestIndexedMigrationHarness::test_evas_simulate_logs_indexed_arrays_when_opted_in -q
python3 -m pytest tests/test_indexed_backend.py tests/test_netlist.py -q
python3 -m pytest tests -q
git diff --check
```

Results:

```text
2 passed in 0.46s
1 passed in 0.64s
91 passed in 0.64s
449 passed in 31.83s
git diff --check: clean
```

Observed metadata:

```text
real x = 1.25;
integer code = 2;
genvar i;
real accum[3:0];
integer bins[0:2];

_state_scalar_names = ("x", "code", "i")
_integer_state_names = ("code", "i")
_state_array_ranges = (
  ("accum", 0, 3, False),
  ("bins", 0, 2, True),
)
```

Indexed model IO plan:

```text
state_scalar_ids = (0, 1, 2)
state_array_layouts = [
  accum: lo=0, hi=3, length=4, integer=False,
  bins:  lo=0, hi=2, length=3, integer=True,
]
```

Interpretation:

- 020 proves state layout can be extracted without changing runtime behavior.
- Scalar state ids are model-local, not global across the whole simulator.
- Array ranges are normalized to inclusive low/high order, so `[3:0]` and `[0:3]` can be represented consistently.
- Integer state is explicitly marked so Rust ABI can preserve Verilog-A integer coercion rules later.

## Functional Safety

- Default backend changed: `no`
- Default generated runtime code changed: `no`
- Runtime state storage changed: `no`
- Integer coercion changed: `no`
- Array bounds behavior changed: `no`
- Event interpolation changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`
- Accuracy impact: `none expected`; full EVAS test suite passed

## Learning Notes

### 为什么 state 也要 indexed？

前面的 017 主要优化 node voltage：

```text
V(vin) -> values[node_id]
```

但模型内部还有大量状态变量：

```verilog
real sample;
integer code;
real accum[3:0];
```

如果 node 已经是数组，但 state 还一直是 Python dict，Rust evaluate 仍然需要频繁回到 Python object 世界，速度收益会被边界开销吃掉。

### scalar state 和 array state 有什么区别？

scalar state 是单个值：

```text
sample
code
```

array state 是一组值：

```text
accum[0], accum[1], accum[2], accum[3]
```

Rust ABI 需要知道 array 的范围和长度，才能把它放进连续数组里。

### 为什么 integer state 要单独标记？

Verilog-A 里 integer 赋值要转成整数。EVAS 目前通过 `_to_integer()` 保证：

```python
self.state["code"] = self._to_integer(value)
```

如果 Rust 以后直接写 state array，也必须知道哪些 slot 是 integer，否则精度/功能会变。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| state layout metadata 漏变量 | `state_scalar_names` / `state_array_layouts` tests 失败 | 回退 EVAS commit `708ebf7` |
| array range 方向理解错误 | array layout tests 或后续 state ABI parity 失败 | 保留 normalized lo/hi，后续单独增加 direction metadata |
| integer state 未标记 | integer coercion parity 失败 | `_integer_state_names` 和 array `integer=True` 必须进入 ABI |
| 把 020 当成 runtime state rewrite | 报告中出现 020 speedup claim | 明确 020 不改 `self.state` / `self.arrays` 执行 |

## Next Step

下一篇建议做：

- `021-rust-model-evaluate-abi-prototype.md`

017-020 已经把 node read/write、event boundary、dynamic bus access、state layout 都暴露成 metadata。021 可以做一个最小 Rust model-evaluate ABI prototype：用简单 static read/write + scalar state layout 验证 Python/Rust 边界、输入数组、输出数组和 fallback 协议。
