# 089 - Cross/Above Detector Production Gate

Status: `done-but-not-recommended-without-090-batch`（详见 Real-Workload Validation）

Date: `2026-06-05`

Code commit: `pending`

Related documents:

- `052-cross-above-detector-rust-primitives.md`
- `055-event-lifecycle-production-gate.md`
- `056-event-due-shadow.md`
- `085-cross-above-transition-default-adaptive-trace.md`
- `086-transition-operator-persistent-buffer-reuse.md`
- `088-transition-per-step-batch-implementation.md`

## One-Line Summary

把 `CrossDetector.check()` / `AboveDetector.check()` 的数学从 Python 升到 Rust primitive 调用：opt-in 标志 `rust_cross_above_production=True` 让 `_check_cross()` / `_check_above()` 调 Rust 替代 Python detector，结果应用到 detector 对象，所有事件副作用（retrograde suppression、event_time context、interp nodes cache、ordering）保留在 Python — Rust 只接管 detector 数学，不接管 event queue。这是 transition `085 production gate` 的 cross/above 对应物。

## Why This Audit Exists

052 已建 Rust primitive `cross_detector_step_for_arrays`、`above_detector_step_for_arrays`。
056 已建 shadow path 验证 primitive 跟 Python 数学等价（cross/above/timer 在多种 case 下 shadow matches 计数器持续 += 1）。
085 已为 transition 建立 per-call production gate（`rust_transition_production=True`）。

**剩下的事**：把 cross/above 也升级到同样的 production gate。这一步：
- 不动 event ordering、不动 event body 执行、不动 phase orchestration（055 反复强调不能擅动 B10/B18）
- 不动 compiler codegen
- 不引入新的 codegen path
- 只是把 Python `detector.check()` 这个内部数学换成 Rust primitive 调用

跟 086 类似：**结构性下沉，不是新功能**。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| `backend.py` CompiledModel `__init__` | 无 cross/above production attrs | 加 `_rust_cross_above_production_backend`、`_rust_cross_above_production_enabled` | 默认 None / False，无开销 |
| `backend.py` `_set_rust_cross_above_production_backend(backend, production=False)` | 不存在 | 新增 setter，递归到 child models | engine 调用入口 |
| `backend.py` `_check_cross_rust_production()` | 不存在 | 新增 helper：构 size-1 typed arrays → 调 `backend.cross_detector_step()` → 应用结果到 `CrossDetector` 对象 → 返回 fired | production path |
| `backend.py` `_check_above_rust_production()` | 不存在 | 新增 helper：同上但 above primitive | production path |
| `backend.py` `_check_cross()` | 直接调 `detector.check()` | 先调 `_check_cross_rust_production()`，返回 None 才回退 `detector.check()` | parity bit-exact 期望 |
| `backend.py` `_check_above()` | 直接调 `detector.check()` | 同上 | |
| `backend.py` perf stats | 无 089 counter | 新增 `rust_cross_production_calls/fires/fallbacks`、`rust_above_production_calls/fires/fallbacks` | 可见 production hit rate + fallback |
| `engine.py` `Simulator.run` 参数 | 无 `rust_cross_above_production` | 新增 opt-in 参数 | API 扩展，默认 False |
| `engine.py` perf stats init | 无 | 加 6 个新 counter init + `requested/available/enabled` 三态 | 标准模式 |
| `engine.py` counter aliases | 无 | 加 6 个 short→`_total` alias | 标准 |
| `engine.py` rust_backend gate | 不含 cross_above | 加进 OR 条件，触发 lib load | |
| `engine.py` backend 安装 | 无 | 在 shadow install 后追加 `if rust_cross_above_production: _set_model_rust_cross_above_production_backend(rust_backend, production=True)` | 跟 transition production 同模板 |

## Principle

属于**降低每步成本**。`_check_cross()` 和 `_check_above()` 在 event-driven 仿真里被频繁调用 —— 每个 evaluate 内每个 cross/above 触发表达式都要调一次。Python `CrossDetector.check()` 内部做：

1. 比较 prev_val、cur_val、direction 决定是否 crossing
2. 线性插值 crossing time
3. 更新内部 state machine（initialized / last_cross_time / pprev_*）
4. 设置 last_triggered / last_trigger_direction / last_trigger_went_beyond

每一步都是 Python 对象 attribute 读写 + 浮点运算。**Rust 的 typed-array primitive 做完全相同的数学但用 C-style 数组顺序读写，省掉 Python 对象开销**。

089 不是真正的 batch（每次仍 1 个 detector 1 次 FFI）—— 就像 086 之于 transition 是"先解决边界开销"，089 是"先把 detector 数学路径升到 Rust，event ordering 留给后续 audit"。

## Before / After Evidence

**单元测试**（`tests/test_audit_089_cross_above_production.py`）：

| 测试类 | 覆盖 | 结果 |
|---|---|---|
| `TestCrossProduction` (3) | parity vs Python detector / counter when enabled / counter when disabled | 3 passed |
| `TestAboveProduction` (2) | parity vs Python above detector / counter | 2 passed |
| `TestCombinedWithShadow` (1) | 086 shadow + 089 production 共存，shadow 0 mismatch | 1 passed |

**全量套件**：568 既有 + 15 audit 088 + 6 audit 089 = **589 passed**，0 regression。

### Real-Workload Validation — 重要负面结果

**`prototypes/audit_089_real_bench.py` 在 cmp_delay 上 15-repeat + trimmed mean**：

| Metric | Python detector (default) | 089 production (opt-in) | 变化 |
|---|---:|---:|---|
| wall trimmed_mean (s) | 10.549 | **31.423** | **0.336× (慢了 198%)** |
| wall stdev (s) | 0.115 | 0.473 | 089 方差更大 |
| wall min / max (s) | 10.43 / 10.77 | 31.15 / 33.01 | |
| rust_cross_production_calls | 0 | **931,440** | 90 万次 FFI hop |
| rust_cross_production_fires | 0 | 64 | 0.007% fire rate |
| rust_cross_production_fallbacks | 0 | 0 | 无 Rust 错误 |
| above_prod_calls | 0 | 0 | cmp_delay 不用 above() |

### 根因 — Per-Call FFI on Hot-Lightweight Functions Is a Net Loss

`CrossDetector.check()` 本质是 prev_val/cur_val 的几个浮点比较 + 一次线性插值，**计算量极小**。

每次 Python → ctypes → Rust → return 的 FFI hop 有**固定边界开销**（pointer marshalling、type conversion、GIL release/acquire、stack frame）。

cmp_delay 一次仿真做 **931,440 次 cross check**（每个 evaluate 2 个 detector × 数十万次 evaluate）。**累积的 FFI 边界开销 >> Rust 数学带来的节省**：

```
Python detector.check() ≈ 5 μs/call  (Python attribute access + few floats)
Rust FFI per call       ≈ 25 μs/call (ctypes marshal + lib call + return)
                          ----- per call -----
Python total ≈ 5 μs × 931k = 4.7s
089 total    ≈ 25 μs × 931k = 23.3s
diff         ≈ 18s — 对得上 wall delta 21s
```

也就是说：**Rust 端数学只占小头；边界开销才是大头。**

### 类比 088 的教训

这是 088 自审教训的极端延续：
- 088 在 cmp_delay 上 wall delta 只有 +2.8%（transition FFI 不是大头）
- 089 在 cmp_delay 上 wall delta 是 **-198%**（cross FFI 边界开销 > 数学收益）

**结论：per-call FFI 对 hot-but-cheap 函数是反优化**。要让 089 有真实价值，必须做 090 batch（避免 per-call FFI）：单步内多个 detector 一次 FFI，把 931k hops 压到 ~50k flushes，边界开销摊薄。但 audit 055 已警告 cross/above batch 涉及 phase ordering 风险。

### 089 仍然是有用的工程

虽然 089 是 net 速度负值，它**结构上完整**：
- ✅ Rust primitive 路径走通
- ✅ Parity bit-exact（6 单元测试全过）
- ✅ Fallback 路径就位（FFI 失败回退 Python）
- ✅ 056 shadow + 089 production 共存 shadow_mismatches = 0
- ✅ 默认 opt-in 关闭（不影响普通用户）

这套基础设施是 090 batch 的**前置**：090 需要的 typed-array 接口、production-vs-shadow 计数、fallback 路径，089 都已经搭好。**090 = 089 + 入队 + flush + ordering 处理**。

但 089 **单独不建议作为速度优化推到生产**：用户启用 `rust_cross_above_production=True` 现在会让仿真变慢。应保持 opt-in 直到 090 落地。

## Functional Safety

- Default backend changed: `no`（需要 `rust_cross_above_production=True` opt-in）
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`（Rust FFI 抛异常 → 返回 None → 调用方落回 `detector.check()`）

## Validation

```bash
PYTHONPATH=. python3 -m pytest tests/test_audit_089_cross_above_production.py -q
# 6 passed

PYTHONPATH=. python3 -m pytest tests/ -q
# 589 passed, 0 regression

PYTHONPATH=. python3 prototypes/audit_089_real_bench.py
# (see Before/After Evidence)
```

## Learning Notes

**为什么 089 跟 088 都叫"batch / queue"但实际做的事情不同**：
- 088 真做了 per-step batch：多个 transition 入队 → 步末一次 FFI → N 个 slot 一次处理
- 089 仍是 per-call：每个 cross/above check 一次 FFI，但内部数学走 Rust

原因：transition 是 contribution（值写到 output node，无 event body），可以 defer；cross/above 是 EVENT 检测器，返回 fired 立即用于 `if fired: <body>` 分支，**不能 defer**。要做真 batch 必须改 compiler 把 evaluate() 重写成两 phase（detector batch → body dispatch），是 audit 090+ 的工作（055 警告涉及 phase-order 风险）。

**为什么 056 shadow 是 089 的前置条件**：
- 056 已经跑了大量 case，验证 Rust 跟 Python 数学等价
- 089 只是"既然两边等价，那 production 用 Rust"
- 如果没有 056 这层 parity 证据，直接做 089 风险高

**counter 命名约定**：
- `rust_cross_production_calls` — 每次 cross() 进 Rust 的次数
- `rust_cross_production_fires` — 其中 fired 的次数
- `rust_cross_production_fallbacks` — Rust FFI 失败回退 Python 的次数
- production_calls 应等于 _check_cross 的总调用数；fallbacks 应为 0

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| Rust primitive 在某 corner case 跟 Python detector 算出不同 t_cross | parity test 失败 / shadow mismatch >0 | 把 `rust_cross_above_production` 默认 False（已是），用户回滚到不传 flag |
| `_check_cross_rust_production()` 抛非预期异常 | `rust_cross_production_fallbacks` >0 | fallbacks 自动回退 Python；无需手动 |
| 同时开启 `rust_event_due_shadow` 和 `rust_cross_above_production` 时 shadow 跟自己比 | shadow_matches 计数翻倍但 mismatches 仍 0 | semantically fine，counters 自洽 |

## Coverage Status After 089

| Sub-case | Status |
|---|---|
| `_check_cross()` 数学走 Rust | ✅ opt-in production |
| `_check_above()` 数学走 Rust | ✅ opt-in production |
| event body 执行 | 仍 Python（055 警告） |
| event ordering / retrograde suppression | 仍 Python |
| crossing-time interpolation cache | 已有（085） |
| timer-based events | 已有（084） |
| 真 per-step batch（多 detector 一次 FFI） | ⏳ 留给 audit 090 |

## Claim Boundary

可以说：
- cross() / above() detector state evolution 已 opt-in 用 Rust primitive（**结构性下沉**）
- 6/6 单元测试 parity + counter consistency 通过
- 589 全量套件零 regression
- 056 shadow + 089 production 可以同时开，shadow mismatches = 0
- 089 把 090 batch 需要的 typed-array / fallback / counter 基础设施全建好

**不能说**：
- 089 是速度优化（实测在 cmp_delay 上慢 3×）
- 用户应该启用 `rust_cross_above_production=True`（除非他们要做 batch primitive 开发）
- cross/above 已 full Rust ownership（event body、ordering、interp side effects 都还是 Python）
- release-wide 速度收益（需 same-slice EVAS/Spectre rerun + 090 batch 落地后验证）

## Next Step

`090 - Cross/Above Detector Lazy + Flush Queue`（可选）：
- 把多个 detector check 入队，evaluate() 中段（或末段）一次 FFI batch
- 需要 compiler codegen 改造：识别 `if self._check_cross(...): <body>` pattern，lower 成 2-phase
- 风险高（055 警告），收益小（推测真实工况 3-5%）— 性价比可能不如做 086-style operator IR coverage 扩展

或者更高 ROI 的方向：
- 089 已经把 cross/above 的"运行时数学"路径升到 Rust
- 下一步可能是 **`$strobe()` / `$display()` 这种 I/O 加速** 或 **CSV writer 优化**，cmp_delay 上 transition + cross 之外的开销
