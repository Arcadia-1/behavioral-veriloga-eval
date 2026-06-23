# 057 Event Trace And Write-Set Audit

## 状态

`done`，默认关闭，不改变正常 EVAS 仿真路径。

## 为什么做

056 只证明 Rust primitive 能复算 `cross/above/timer` 是否 due，但这还不能让 event queue 或 event body 进入 Rust。真正阻塞 production Rust 化的是另一件事：事件触发后，事件体到底按什么顺序执行、写了哪些 state/array/output/timer/transition 状态。

本轮把这些副作用收成一个 opt-in audit 层：

- `EVAS_EVENT_TRACE_AUDIT=1` 或 `evas_event_trace_audit=true` 开启。
- 记录 fired event 的 phase、kind、key、step time、event time。
- 记录 event body enter/exit。
- 统计 state、array、output、timer state、timer last-fired、transition、transition-output 写入。

这不是速度优化本身。它的作用是把后续 Rust event/evaluate batch 的 correctness boundary 固化下来，避免继续凭感觉迁移。

## 改前状态

事件相关信息分散在多个 Python 路径：

- `_check_cross/_check_above/_check_timer*` 负责 due 判断。
- `_compile_event_statement` 和 `_compile_post_update_event_statement` 负责生成 event body。
- `_state_set/_array_set/_set_output/_transition/_set_timer_state` 分别写不同 runtime 容器。
- 少数快路径会绕过 helper，例如 for-loop state 写入、state-local fastpath 尾部回写、Rust static output sync。

因此我们很难回答一个真实 benchmark 的问题：某一轮仿真里，event body 写入占多少、写了哪些域、哪些写入必须跟 event queue 一起进入 Rust。

## 改后状态

新增 `CompiledModel` 侧审计入口：

- `_set_event_trace_audit_enabled()`
- `_event_trace_audit_record_event()`
- `_event_trace_audit_enter_event()`
- `_event_trace_audit_exit_event()`
- `_event_trace_audit_note_write()`

新增 `Simulator.run(event_trace_audit=True)` 和 runner 环境变量 `EVAS_EVENT_TRACE_AUDIT=1`。

写入覆盖：

| 写入域 | 当前入口 | 057 覆盖状态 |
|---|---|---|
| scalar/integer state | `_state_set`, `_state_set_by_slot` | covered |
| for-loop state target | `_compile_assignment` 生成 `_state_set` | covered |
| state-local fastpath final writeback | generated evaluate tail | audit-only covered |
| array state | `_array_set` | covered |
| output contribution | `_set_output`, static branch helpers | covered |
| Rust static output sync | engine `_sync_rust_static_outputs` | audit-only covered |
| timer next-fire | `_set_timer_state` | covered |
| timer last-fired | `_set_timer_last_fired` | covered |
| transition state | `_transition` mutation points | covered |
| transition fused output | `_transition_output` | covered |

事件覆盖：

| 事件域 | 当前入口 | 057 覆盖状态 |
|---|---|---|
| `cross()` | `_check_cross` + generated event body wrapper | covered |
| `above()` | `_check_above` + generated event body wrapper | covered |
| periodic `timer()` | `_check_timer_due/_check_timer` + generated wrapper | covered |
| absolute `timer()` | `_check_timer_at` + generated wrapper | covered |
| `initial_step` | generated `initial_step()` body wrapper | covered |
| `final_step` | generated `final_step()` body wrapper | covered |
| post-update cross/above | generated `post_update_events()` wrapper | covered |
| combined event | generated combined-event wrapper | covered |

## 验证

Targeted checks:

```text
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache PYTHONPATH=EVAS python3 -m py_compile EVAS/evas/simulator/backend.py EVAS/evas/simulator/engine.py EVAS/evas/netlist/runner.py
PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_engine.py::TestSimulator::test_event_trace_audit_records_generated_event_body_writes EVAS/tests/test_engine.py::TestSimulator::test_rust_event_due_shadow_matches_cross_above_and_timer_checks -q
PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_netlist.py -k event_trace_audit -q
```

当前结果：

- engine targeted: `2 passed`
- netlist targeted: `1 passed, 77 deselected`
- py_compile: pass

## 对速度的影响

默认关闭，因此正常 benchmark/speed path 不应因为 057 增加 trace storage 或 event records。

打开 audit 后会有额外 Python list/dict 写入，只用于诊断，不应参与 paper-facing speed claim。

## 学习备注

可以把 EVAS 当前事件系统理解成三层：

1. detector：判断 `cross/above/timer` 是否触发。
2. dispatch：按当前 Python 生成代码顺序进入 event body。
3. side effect：event body 修改 state/array/output/timer/transition。

Rust 化不能只搬第 1 层。只搬 detector 最多减少 due 判断开销，但 event body 仍要回到 Python dict/object。要获得大收益，必须让第 2 和第 3 层也能进入 typed array / Rust batch。

## 下一步

停止继续做零散 shadow。下一步应直接做 production 候选：

1. 用 057 audit 在 top-wall benchmark 上采样 event body write-set 分布。
2. 选择最多见的 event-body 写入形态，先把 `state/array/output` assignment lowering 到 typed write ops。
3. 把 fired event order + write ops 放进同一个 Rust batch 做 shadow parity。
4. parity 通过后，再做 opt-in production fastpath。

如果 audit 显示 event-body 写入很少，则优先回到 generated model evaluate 全量 IR；如果 event-body 写入很多，则 event queue/write-set production 是 P1。
