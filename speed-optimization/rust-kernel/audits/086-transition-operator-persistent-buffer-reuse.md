# 086 - Transition Operator Persistent Buffer Reuse

Status: `done`

Date: `2026-06-05`

Code commit: `pending`

Related documents:

- `050-transition-state-rust-primitive.md`
- `085-cross-above-transition-default-adaptive-trace.md`
- `../RUSTIFICATION_WORKLIST_20260605.md`

## One-Line Summary

`_transition_rust_production()` 把 14 个 size-1 `array("d", [...])` typed-array buffer 从"每次调用新建"改成"backend 持有一份持久化 buffer，所有调用复用"；FFI 调用次数和 Rust 数学完全不变，但 Python 端 buffer 分配从 N×14 降到 14，bench 上 transition-heavy 模型 wall 提速 **1.135×（约 12%）**，输出 bit-exact parity。

## Why This Audit Exists

085 把 `_transition()` 的 production path 接到 Rust（`rust_transition_production=True`），但保持了 per-call typed-array 分配：每次 `_transition(key, ...)` 调用都执行 14 次 `array("d", [...])` 分配。

新 worklist 把 transition 列为 L2 operator-batch 的下一步。真正的 per-step batch（"一步内所有 transition 合一次 FFI"）受限于 `_transition()` 必须**立即返回值**给 compiled model 表达式 — 这需要改 compiler codegen 把 `transition()` lower 成 deferred placeholder + step-末 flush，是 audit 087+ 的工作。

本 audit（086 = L2-a）做"持久化 buffer"这一稳赢小步：FFI 计数和顺序不变、Verilog-A 语义不变，只消除 hot loop 的重复 alloc。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| `EVAS/evas/simulator/backend.py` `_transition_rust_production()` | 每次 call 新建 14 个 size-1 `array` | 首次 call lazy-init 一份持久 buffer dict 挂在 `self._rust_transition_buffers`，后续 call 直接复写元素 `[0]` | 默认 backend 不变；opt-in `rust_transition_production=True` 路径 waveform bit-exact 一致 |
| `EVAS/evas/simulator/backend.py` perf stats | `rust_transition_state_production_calls/outputs/fallbacks` | 新增 `rust_transition_state_buffer_reuse_calls`、`rust_transition_state_buffer_alloc_total` | runner 可见 buffer 复用次数和分配总数 |
| `EVAS/evas/simulator/engine.py` counter aggregation | 没有新 counter 的 `_total` 别名 | 加 `rust_transition_state_buffer_reuse_calls_total`、`rust_transition_state_buffer_alloc_grand_total` | runner 报告里能取到这两个数 |
| `EVAS/prototypes/audit_086_bench.py` | 不存在 | 新增 baseline-vs-new 对照 bench，通过 monkey-patch 强制 baseline 走 per-call realloc | 可重跑、可审计 |

## Principle

属于**降低每步成本**。`_transition()` 在 transition-heavy 行（如 cmp_delay、SAR、CPPLL）每步会被调用多次，每行 simulation 累积调用数从几千到几万。原路径每次都执行：

```python
current_values = array("d", [float(ts.current_val)])   # alloc
target_values  = array("d", [float(ts.target_val)])    # alloc
# ... 12 more ...
```

14 次 `array("d", [single_float])` 不是 free — 每次都要：

1. CPython 对象 header 分配
2. typecode 解析
3. 单元素 buffer alloc
4. `__init__` 调用
5. 后续 GC tracking

把这 14 次乘以几万次调用，就是真实的 hot-loop 开销。本 audit 把这部分摊销到一次性 lazy init。

## Before / After Evidence

Bench：`EVAS/prototypes/audit_086_bench.py`，5 repeats，tstop=50ns，tstep=50ps，record=100ps，transition-heavy 单模型（`q = V(inp) > 0.45; V(out) <+ transition(...)`）。

| Metric | Baseline (force per-call realloc) | Audit 086 (persistent buffer) | Interpretation |
|---|---:|---:|---|
| wall median (s) | 0.691813 | 0.609392 | **1.135× faster (≈12%)** |
| wall min (s) | 0.672202 | 0.606890 | bench-noise floor 也下降 |
| wall max (s) | 0.959036 | 0.711722 | tail 也压缩 |
| FFI calls | 23,317 | 23,317 | **identical** — 不是减 FFI |
| `array()` allocs | **326,438** | **14** | **23,317× fewer** |
| buffer reuse calls | 23,317 | 23,317 | 与 FFI calls 一致 |
| output checksum | 494.499296260 | 494.499296260 | **bit-exact parity** |
| pytest 全量 | 568 passed | 568 passed | 无 regression |

宏观解读：

- **Rust 端 0 改动**，所有数学保持原样
- **Python 端 alloc 数从 326k 降到 14**（同一模型一次完整 run）
- **wall 提速 ~12%** — 完全来自消除 hot loop alloc / GC pressure
- **parity bit-exact** — 不是近似一致，是浮点逐位相同

## Functional Safety

- Default backend changed: `no`（仍需 `rust_transition_production=True` opt-in）
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`（FFI 抛异常时仍 fallback 到 Python TransitionState；`_rust_transition_buffers` 不影响 fallback 路径）

## Validation

Commands run:

```bash
PYTHONPATH=. python3 -m pytest tests/test_engine.py -k 'transition' -q
PYTHONPATH=. python3 -m pytest tests/test_rust_backend.py -q
PYTHONPATH=. python3 -m pytest tests/ -q
PYTHONPATH=. python3 prototypes/audit_086_bench.py
```

Results:

```text
tests/test_engine.py -k transition  : 37 passed
tests/test_rust_backend.py          : 34 passed
tests/ (全量)                       : 568 passed in 38.00s
prototypes/audit_086_bench.py       : 1.135× speedup, parity bit-exact, 23,317× fewer allocs
```

## Learning Notes

**什么是 typed array？**
Python 标准库的 `array.array("d", ...)` 是一个连续 `double` buffer，可以直接传给 ctypes 函数当 `double*`。比 `list` 更接近 C，但创建它仍要走 Python 对象分配。

**为什么 14 个？**
Rust `transition_state_step_for_arrays` 签名要 14 个 typed array 参数（current/target/start_time/start_val/delay/rise/fall + active/init 两个 u8 flag + 4 个 input + 1 个 output）。每次 FFI 调用都要传这 14 个指针，所以原代码每次都新建 14 个。

**为什么 buffer 可以复用？**
因为 FFI 是同步的：调用进去 → Rust 写 → 调用返回 → Python 读。下一次调用前，buffer 内容已经被读出写到 `TransitionState` 对象。所以 buffer 只是个"消息信封"，不需要每次新做一个。

**为什么不直接做"一步内 batch"？**
`_transition()` 是被 compiled model code 内联调用的：
```python
v_out = self._transition("k", t, target_val, ...)  # 立刻要值
contribute(f(v_out))                               # 下一行就用
```
如果延后到 step 末统一调 Rust，`v_out` 还没算出来。要做真 batch 必须改 compiler 把这种调用 lower 成 deferred placeholder + 步末 resolve。那是 audit 087 的工作量。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| 多线程同时调 `_transition_rust_production()` 写同一个 buffer | 数据 race / parity 失败 | EVAS 当前 backend 是 single-threaded；如果未来引入多线程，需把 buffer 改成 thread-local。回滚：把 `_rust_transition_buffers` 改回 None init + per-call alloc |
| buffer 持久持有阻止 backend 被 GC | memory growth in long-lived process | buffer 大小是 14 × 8 bytes ≈ 100 bytes / backend，可忽略 |
| 复用 buffer 时上一次值残留导致语义错 | parity test fail | 每次调用都全 14 字段 overwrite，不读旧值。已经被 bit-exact parity 验证 |

## Claim Boundary

可以说：
- transition operator 的 Python 端 per-call allocation overhead 已被消除
- 对 transition-heavy 单元 bench wall 提速 ~12%，parity bit-exact
- alloc count 从 23k+ 降到 14（一次性 init）

不能说：
- EVAS Rust path 已经 paper-facing 快于 Spectre AX
- transition 已经 full Rust ownership（仍是 per-call FFI，不是 batch；compiler codegen 仍生成 Python 调用）
- release-wide 速度收益（需 same-slice EVAS/Spectre rerun 验证）

## Next Step

`087 - Transition Operator Per-Step Batch Via Codegen`：把 compiler 生成的 `self._transition(...)` 调用 lower 成 deferred placeholder + 步末 flush 模式，让一步内 N 次 transition 真正合成 1 次 Rust FFI。这是 L2-b，需要：

- 改 codegen：识别 transition() 表达式，emit 一个 "request transition value" 占位 + 后续 resolve
- 改 backend：维护"本步内 pending transition list"，evaluate 末统一 Rust batch
- 风险：transition 返回值会被立即用于 `contribute()` — 需要确认 contribute 也是步末 flush（如果不是，必须保持 fallback）

预计 wall 提速 5-15% 额外（在 086 之上），FFI 调用从 N→1（per step）。
