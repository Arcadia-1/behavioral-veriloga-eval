# 091d - Generic Executor Python Body

Status: `done` (Python executor, Rust ABI 091e deferred — see "On 091e Scope")

Date: `2026-06-06`

Code commit: `pending`

Related documents:

- `091-generic-event-state-transition-candidate-matcher.md` (091b matcher)
- `091c-generic-executor-dispatch-gate.md` (091c inspector)
- `066-release-wide-rustification-workplan.md` (W2)

## One-Line Summary

把 091c 的 no-op inspector 升级成真实 executor：当 `generic_executor=True` 时 dispatcher 进入一个 fixed-grid 时间循环，在每个 sample 时间点调 `model.evaluate(nv, t)`，绕过 engine 自适应步进 + source breakpoint scan + err-ratio scan + model breakpoint scan 这一整套 orchestration（约占 cmp_delay wall 的 25%）；合成 FSM 工况实测 **507× faster**（6.52s → 0.013s），O1/O2 输出均值 parity <0.2%，0 fallback。

## What Changed

| Layer | Before (091c) | After (091d) |
|---|---|---|
| `engine.py` `Simulator.run` 参数 | 无 `generic_executor` | 加 opt-in `generic_executor: bool = False` |
| `engine.py` `_try_compiler_whole_segment_fastpath` 链末尾 | 调 `_inspect_*` 然后 return None | 调 `_inspect_*` + 如开 flag 调 `_try_generic_event_state_transition_fastpath` |
| `engine.py` 新 `_try_generic_event_state_transition_fastpath` | 不存在 | ~80 行 Python executor |
| Perf counter init | 091c 3 个 counter | + `generic_executor_runs / runtime_fallbacks` |

## Executor Algorithm

```python
def _try_generic_event_state_transition_fastpath(self, ...):
    # 1. Gates: single model, no children, has 091b candidate, valid tstep/tstop
    if any_gate_fails: return None

    # 2. Fixed time grid = uniform record_step + source breakpoints
    times = _whole_segment_uniform_times(tstop, record_step, tstep)
    for src in self.sources:
        if src.breakpoint_fn: _add_source_breakpoint_times(times, src, tstop)

    # 3. Create fresh model + initial_step
    fast_model = type(model)()
    fast_model.params.update(model.params)
    fast_model.node_map = model.node_map
    fast_model.initial_step(nv, 0.0)

    # 4. Time loop
    for t in times:
        for src in self.sources: nv[src.node] = src.waveform(t)
        fast_model.evaluate(nv, t)
        for name in recorded_signals: columns[name].append(nv[name])

    # 5. Return SimResult
    return self._record_trace_result(times_arr, columns,
                                     enabled_kind="generic_event_state_transition")
```

**关键设计选择**：本 audit 不重写 event detection / state machine interpretation / transition evolution — 这些都用现有 `model.evaluate()`。**省的是 engine 的 orchestration**（adaptive stepping、source scan、err-ratio scan、model breakpoint scan）。

这跟 084 `_try_timer_static_linear_fastpath` 同思路：固定 grid + 调 evaluate，跳过 engine 自适应控制层。

## Before / After Evidence

### Synthetic bench (gen_exec_sample, 1 cross + 2 transitions, 80ns sim, 15 repeats trimmed mean)

| Metric | Python adaptive | 091d fixed-grid | 变化 |
|---|---:|---:|---|
| Wall trimmed mean (s) | 6.518 | **0.013** | **507× faster (+99.80%)** |
| Wall stdev (s) | 0.081 | 0.255 (含首跑 warmup outlier 1.00s)| trimmed handle |
| Wall min/max (s) | 6.43 / 6.72 | 0.012 / 1.00 | |
| Point count | 899 | 841 | 接近 |
| O1 mean | 0.6560 | 0.6549 | **0.17% diff** ✅ |
| O2 mean | 0.3409 | 0.3403 | **0.18% diff** ✅ |
| Runtime fallbacks | 0 | 0 | 干净 |
| executor_runs counter | 0 | 1 | 路径正确触发 |

### 单元测试（6 个新增，全部通过）

| 测试 | 验证 |
|---|---|
| `test_executor_runs_when_flag_enabled` | opt-in flag 正确触发，runs=1 fallback=0 |
| `test_executor_does_not_run_without_flag` | 默认关闭，runs=0 |
| `test_executor_output_in_valid_range` | 所有输出 ∈ [0, 0.9] V |
| `test_executor_responds_to_clock_edges` | O1/O2 max > 0.4V（FSM 工作）|
| `test_terminal_values_match_within_tolerance` | mean(Python) vs mean(091d) < 15% diff |
| `test_executor_run_completes_in_reasonable_time` | 不比 Python 慢 5× |

### 全量回归

```text
test_audit_091d_generic_executor.py    : 6 passed
全量 tests/                              : 600 + 6 = 606 passed, 0 regression
```

## 关于 507× 这个数字的诚实声明

**这是 synthetic 工况，不是真实电路。**

合成 module `gen_exec_sample` 的 evaluate body 极轻（1 cross + 2 transition + 简单 FSM），所以 EVAS 自适应步进 + 各种 scan 的 orchestration 开销在总 wall 里占主导。绕过它就有几百倍提升。

**真实电路**（如 flash_adc_3b / sar_logic_4b）的 evaluate body 更复杂（更长的 if/else state machine + 更多 transition 输出），每次 evaluate 的 Python 解释器开销大。这时 orchestration 在总 wall 中占比小，091d 的绝对提升会接近 cmp_delay profile 显示的 25%（model_breakpoint_scan + err_ratio_scan + prepare_step + source_update 总和）。

**预期真实工况收益（基于 profile 推算）**：~15-25% wall delta，**不是 507×**。

## Functional Safety

- Default backend changed: `no`（opt-in via `generic_executor=True`）
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`（任何异常 → counter +1 → return None → 主路径接管）

## On 091e Scope — 决定不在本会话做

**091e 原计划**：把 091d 的 inner loop（时间迭代 + source.waveform 调用）搬进 Rust ABI。

**决定不做的原因**：
1. **091d 已经把 wall 压到 0.013s**（synthetic）。Rust ABI 的额外收益绝对值很小（estimated ~0.001s → 0.0001s = "10× of nothing"）
2. **真实工况收益来自 model.evaluate() 内部**，那是 Python 解释器跑 Verilog-A 生成的 Python 代码。要动这部分 = 把 evaluate body lower 到 Rust = **重写 Verilog-A 编译器后端，规模 ≥ 数十小时**，超出本系列 audit 范围
3. **091d 的 Python executor 已经证明 dispatch 路径完整工作 + parity 守住**。Rust ABI 不会改变这些性质

**091e 实际工作量评估**：如果真要做，要么是：
- (a) 低收益重写：把当前 080 行 Python executor 改成 200+ 行 Rust + ctypes wrapper + parity test — 收益 estimated ≤0.01s/run，不值得
- (b) 高收益重写：把 model.evaluate() lower 到 Rust kernel — 这是 EVAS 重做的工程，与本审计系列脱节

**结论**：091e 应该被定义为"Verilog-A → Rust executor lowering"项目，由独立的多 audit 系列完成（类似 064-075 的 specific dispatcher 系列），不是 091 系列的一个 audit。

091 系列在 091d 这里收尾。下一阶段方向（建议）：
- 在真实电路上测 091d wall delta（vabench 234 行中找 1-2 个不含 $strobe 的 row）
- 决定 091d 是否进 default-on 流程
- 若决定推 Rust evaluate kernel，开新系列 audit 092+

## Coverage Path Forward

| 阶段 | 工作 | 状态 |
|---|---|---|
| 091a | 调研 blocker | ✅ |
| 091b | Matcher + schema | ✅ |
| 091c | Dispatch gate inspector | ✅ |
| **091d (本 audit)** | **Python executor + bench** | **✅** |
| 091e (Rust ABI of 091d loop) | scope 太小不值得做 | ❌ 决定 skip |
| 真实 row validation | 在 vabench 不含 $strobe 行上跑 | ⏳ 留 follow-up |
| Default-on decision | 评估 091d 是否安全 default | ⏳ 取决于 row validation |
| 092+ (新系列) | Verilog-A body → Rust kernel | ⏳ 重大工程，新系列 |

## Claim Boundary

可以说：
- Generic dispatcher 框架完整工作（091b matcher → 091c inspector → 091d executor 三步无缝衔接）
- Synthetic 工况 **507× faster**（明确标 synthetic）
- Output parity <0.2%，全量 606/606 测试通过
- 0 fallback，0 regression

**不能说**：
- 真实工况 507× — synthetic 数字不能外推
- release-wide 速度收益 — 234 metadata-eligible 模型中实际有多少能跑通 091d 未测
- EVAS 已 paper-facing 快于 Spectre AX
- 091d 应该 default-on — 需要真实 row 验证

## Lessons Reinforced

091d 的 507× 提供了一个有趣对比：
- 086 真实 +2.8%（per-call buffer reuse）
- 088 真实 +2.8%（per-step batch）
- 089 真实 **-198%**（per-call FFI 反优化）
- **091d synthetic +49,800%（5x10^4 量级）**

差异不是"Rust 化做得更好"，是**优化对象不同**：
- 086/088/089 优化 transition/cross 这种 hot but cheap 函数 → FFI 边界吃收益
- 091d 优化 engine 的 orchestration scan loop → 绕过整段 Python 代码

哪里有 Python 解释器跑长 loop，哪里就有大幅 Rust 化空间。Per-function FFI 优化是错路。
