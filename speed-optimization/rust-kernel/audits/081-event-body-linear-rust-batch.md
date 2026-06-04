# 081 Event Body Linear Rust Batch

## 核心结论

这一轮把 `cross/above/timer` 触发后的简单 event body 从“只有 LFSR 特化模板能进 Rust”扩展为通用 static-linear state write-set batch：

- `count = count + 1`
- `toggle = 1.0 - toggle`
- `state = V(inp) > th ? high : low`
- 固定下标 state array 赋值和静态 `for` 展开后的有序赋值

这些 event body 现在会被 compiler lowering 成已有 `RustLinearOp` batch，并在 `rust_event_write_shadow=True` 或 `rust_event_write_production=True` 时执行。默认 backend 不变。

这还不是完整 event queue Rust 化。`cross()` / `above()` 的 due 判断、crossing-time interpolation、同一步多事件排序、refine step 仍由 Python 拥有；本轮只把“事件已经触发后，body 如何写 state”这一层批量下沉。

## 改造原理

event body 的简单赋值可以表示成有序线性写：

```text
target_state = condition ? (bias + sum(gain_i * source_i))
                         : (false_bias + sum(false_gain_i * source_i))
```

这正好复用 037 之后已有的 `evaluate_static_linear` Rust ABI。和连续 evaluate 不同，event body 是离散执行的，所以自依赖更新是安全的：

```text
count = count + 1
toggle = 1 - toggle
```

Rust batch 按 op 顺序读取旧 state、写入新 state，语义等价于 Python event body 的顺序赋值。

## 正确性边界

### 为什么 cross body 读节点时先 fallback

`cross()` 触发后，Python event context 可能用 crossing-time 插值值读取节点，而 Rust static-linear batch 当前只能读 indexed node array 的“当前步值”。如果 event body 包含 `V(node)`，直接 production 可能绕过插值语义。

因此本轮的 production gate 是：

- cross body 只要读节点，并且当前 event context 有 interpolation nodes，就 fallback 到 Python body。
- cross body 只读 state/参数/常量时，可以 production。
- above/timer 没有 crossing-time 插值上下文，可以 production 读当前 node array。

### state-local fastpath 同步

`indexed_state_fastpath_codegen=True` 时，Python generated evaluate 会把 state 缓存在局部变量里，最后再写回 indexed state array。Rust batch 读写的是 indexed state array，所以本轮在 generated code 里增加两个同步动作：

- Rust/shadow 执行前，把参与 event body 计算的 local state 刷到 indexed state array。
- Rust production 后，把被写 target state 刷回 Python local state，防止函数末尾 local flush 覆盖 Rust 结果。

这保证 Rust event body 可以和现有 state-local fastpath 共存。

## 改动内容

- `EVAS/evas/simulator/backend.py`
  - 新增 `_event_body_static_linear_ir()`，收集 event body 中可 lowering 的 state assignment write-set。
  - 支持 event body 的 self-dependent state update、`if/else` 条件选择、静态 `for` 展开和固定下标 state array。
  - 新增 `_rust_event_linear_write_shadow_begin/end()` 和 `_rust_event_linear_write_production()`。
  - 新增 generated-code helper，在 LFSR 特化模板之后尝试通用 linear event body batch。
  - 对 cross interpolation + node-read 场景保守 fallback。
- `EVAS/evas/simulator/engine.py`
  - event write candidate 检测加入 `_event_static_linear_ir_ops`。
  - 只有存在线性 event body 候选时才自动打开 indexed arrays，避免扰动旧 LFSR-only fastpath 统计。
  - 新增 `rust_event_linear_write_*` perf counters。
- `EVAS/tests/test_engine.py`
  - 新增 cross state-only event body production/shadow parity。
  - 新增 above node-read event body production parity。
  - 新增 cross node-read event body fallback regression。

## 验证结果

```text
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache PYTHONPATH=EVAS python3 -m py_compile EVAS/evas/simulator/backend.py EVAS/evas/simulator/engine.py
PASS

PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_engine.py -k "rust_event_linear_write or rust_event_write" -q
4 passed, 232 deselected

PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_engine.py -k "timer or cross or above or rust_event_write or rust_event_linear_write" -q
71 passed, 165 deselected

PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_rust_backend.py -q
31 passed

PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_indexed_backend.py -q
41 passed
```

## 速度影响判断

本轮是通用 event body coverage 补齐，不单独 claim release speedup。

它减少的是触发后 event body 内部的 Python assignment / dict / array object 开销。它不会减少：

- 每步触发条件表达式求值；
- `_check_cross/_check_above/_check_timer*` 调用次数；
- cross refine / breakpoint 扫描；
- record/CSV/checker 外层开销。

所以预期收益取决于真实 benchmark 中“触发很频繁、body 是简单线性 state write-set”的占比。对这种模型，收益会比只做 LFSR 特化更通用；对 dominated by event due scan 或 whole-segment trace 的模型，收益可能仍被外层开销压住。

## 仍未完成

| 项目 | 当前状态 | 下一步 |
|---|---|---|
| event due / queue Rust production | 仍由 Python 判定 due 和 event order | 需要把触发表达式、detector state、due mask、body batch 合成同一段 typed-array loop |
| cross interpolation Rust production | 当前 node-read cross body fallback | 需要 Rust 侧表示 prev/current/future node arrays 和 event-time interpolation policy |
| event body output write | 本轮只 production state write-set | 后续把 `V(out)<+state` / event-owned output write 接到 node array sync |
| dynamic arrays / buses | 动态 index 仍 fallback | 需要复用 B17 dynamic bus offset primitive 和 state array layout |
| complex event body | `while`、system task、非线性函数、child model 仍 fallback | 需要 statement IR 或 whole-segment lowering |

## 下一步

1. 用 top-wall/release coverage manifest 统计 `_event_static_linear_ir_ops` 命中率和 fallback reason。
2. 对高频 event 模型做 event due + body 的 whole-segment batch，而不是继续做 per-event 小 FFI。
3. 将 cross interpolation 所需的 prev/current/future node arrays 和 event-time policy 显式进 Rust ABI。
4. 把 record/snapshot/CSV array path 和 event body output write 合并，避免 Rust 更新后又回到 Python dict/CSV 热路径。
