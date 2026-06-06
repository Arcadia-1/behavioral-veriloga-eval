# 099 - Body IR Rejection Taxonomy

Status: `done`

Date: `2026-06-05`

Code commit: `pending`

Related reports:

- `/private/tmp/evas_rust_coverage_099_tags.json`（本地临时 P0 taxonomy 输出，不是 repo artifact）
- `EVAS/evas/simulator/stmt_ir.py`
- `EVAS/evas/simulator/backend.py`
- `EVAS/evas/simulator/rust_coverage.py`
- `EVAS/prototypes/audit_098_current_rust_coverage.py`

## One-Line Summary

把 P0 覆盖审计从单一 `body_stmt_ops_unsupported` 大桶拆成多标签 taxonomy，确认真实 release 的通用 body IR 缺口主要集中在 `transition()`、event statement、复杂 if/write-set、`$abstime`、`$strobe` 和差分/索引输出目标。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| statement IR diagnostics | `encode_body_stmt_ops()` 只返回 pass/None | 新增 `classify_body_stmt_ops_rejection()`，对失败 body 产出 event/transition/array/loop/system-task 标签 | 仿真默认不变 |
| compiler metadata | 只有 `_rust_body_ir_rejection_reason` | 新增 `_rust_body_ir_rejection_tags` | 只影响 audit metadata |
| coverage audit | 只能统计一个 coarse reason | JSON 额外输出 `rust_body_ir_rejection_tags` 计数 | 只读审计 |
| tests | 只检查 event row 被粗粒度拒绝 | 检查 event row 带 `event_statement` / `event_cross` tags | 默认不变 |

## Principle

这一步不是加速本身，而是让后续加速按证据排序。

之前 348 个 compile-ok release `.va` 全部落在 `body_stmt_ops_unsupported`，这个结论只能说明“没命中”，不能说明“为什么没命中”。现在每个拒绝模型会保留多标签，例如同一个模型可以同时有：

- `event_statement`
- `event_cross`
- `transition_expr`
- `complex_if_write_set`
- `special_identifier:$abstime`

这比单一 reason 更符合真实 Verilog-A：一个 analog block 往往同时包含事件触发、状态更新、transition 输出和 `$abstime` 逻辑。后续应该优先打最高频标签，而不是继续按直觉写小 Rust primitive。

## P0 Taxonomy Result

Release tasks 根目录：

`behavioral-veriloga-eval/benchmark-vabench-release-v1/tasks`

| Metric | Value |
|---|---:|
| `.va` files scanned | 357 |
| compile ok | 348 |
| compile failed | 9 |
| 094 body IR candidates | 0 |
| static linear candidates | 4 |
| whole-segment candidates | 257 |

Top rejection tags:

Primary rejection reasons:

| Reason | Count | Interpretation |
|---|---:|---|
| `event_statement` | 321 | 这些模型第一层就需要 event-phase planner，不能当普通 continuous body 编码 |
| `transition_expr` | 27 | 这些模型没有先被 event 挡住，但仍需要 transition contribution/runtime 进入通用 body path |

Multi-label blocker tags:

| Tag | Count | What it means |
|---|---:|---|
| `transition_expr` | 344 | 几乎所有真实 release model 都有 `transition(...)` 输出或表达式 |
| `event_initial_step` | 321 | 大量模型用 `initial_step` 初始化状态 |
| `event_statement` | 321 | analog block 里有 `@(...)` event statement，当前 body encoder 不接整段 event |
| `event_cross` | 272 | 大量模型靠 cross 边沿触发状态机 |
| `complex_if_write_set` | 172 | if/else 写集合不满足当前 select-lowering 的保守条件 |
| `special_identifier:$abstime` | 95 | 表达式依赖仿真时间，需要把 time 作为 Rust body input |
| `non_numeric_literal` | 76 | 字符串/file handle 等 literal 进入 lowered tree，常见于 logging/system-task 周边 |
| `system_task:$strobe` | 71 | 有输出/日志副作用，不应盲目进纯计算 Rust body |
| `event_timer` | 70 | timer queue 是高频真实缺口 |
| `differential_output_target` | 65 | `V(out, ref) <+ ...` 这种差分贡献 target 当前不支持 |
| `unsupported_binary_operator:>>` | 22 | 位移操作还没进入 body expr ABI |
| `for_loop` | 8 | 固定循环/数组状态机仍被拒绝 |
| `array_assignment_target` | 10 | state array 写入还没进入通用 body write-set |

## Interpretation

这个结果解释了为什么“之前做了很多 event/transition，P0 仍是 0”：

1. `transition_expr` 是 344/348 级别的问题，不能只靠一个 direct-transition shadow runtime 解决。
2. `event_statement` / `event_cross` / `event_timer` 是 321/272/70 级别的问题，必须把 event due、event body 和 source-order phase 组合成同一个 program。
3. `complex_if_write_set` 有 172 个，说明只支持简单 if/else select 不够。真实模型常见多目标写、条件里读写相关 state、或者分支写集合不完全一致。
4. `$abstime` 有 95 个，通用 body IR 需要显式 `time` input；否则 transition target、timer math、measurement flow 都会拒绝。
5. `$strobe` / file IO 这类副作用不应直接 Rust 化，应该作为 fallback 或 side-effect boundary 单独处理。

因此下一步的主线应该是：

```text
analog block planner
  -> event due/order
  -> event body write-set
  -> continuous output / transition contribution
  -> time input + transition breakpoint
  -> persistent typed arrays
```

而不是继续只扩一个局部 primitive。

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`

## Validation

Commands run:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache_099 PYTHONPATH=/Users/bucketsran/Documents/TsingProject/vaEvas/EVAS python3 -m py_compile \
  EVAS/evas/simulator/stmt_ir.py \
  EVAS/evas/simulator/backend.py \
  EVAS/evas/simulator/rust_coverage.py \
  EVAS/prototypes/audit_098_current_rust_coverage.py

PYTHONPATH=/Users/bucketsran/Documents/TsingProject/vaEvas/EVAS python3 -m pytest EVAS/tests/test_engine.py -k "body_ir or rust_coverage" -q

PYTHONPATH=/Users/bucketsran/Documents/TsingProject/vaEvas/EVAS python3 EVAS/prototypes/audit_098_current_rust_coverage.py --json-out /private/tmp/evas_rust_coverage_099_tags.json
```

Results:

```text
py_compile: pass
targeted body_ir/rust_coverage: 3 passed, 243 deselected
release taxonomy sweep: 357 scanned, 348 compile ok, 0 body IR candidates
```

## Learning Notes

这里的多标签不是 bug，而是必要信息。比如一个 PLL/ADC 行可能同时有：

- `event_cross`：边沿来了才更新状态；
- `transition_expr`：输出不能瞬间跳变，需要 ramp；
- `$abstime`：状态机逻辑依赖当前时间；
- `complex_if_write_set`：不同分支写多个状态。

如果我们只看第一个失败点，会误以为“只要修 cross 就好了”。实际上修完 cross 后，transition/time/if 还会继续挡住。所以 099 的作用是把后续工作排序，而不是证明速度。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| taxonomy 误导优先级 | 某标签高频但实际可 fallback，不影响热路径 | 用 top-wall row 交叉过滤，不只看 count |
| diagnostic 代码影响 production | 默认仿真测试失败或 metadata 生成异常 | 回退 `stmt_ir.py` classifier 和 backend metadata 挂载 |
| 多标签 count 被误当 candidate count | 把 `transition_expr:344` 写成 Rust coverage | 保持 claim boundary：candidate 仍是 0 |

## Next Step

`100 - Analog Block Planner For Event-Transition Segments`

目标：不先扩小 primitive，而是新增一个 planner，把常见 analog block 拆成 ordered phases，并计算每个 release model 是否满足：

1. event due 可表达；
2. event body write-set 可表达；
3. continuous output / transition contribution 可表达；
4. `$abstime` 可作为 body input；
5. side-effect system task 可隔离或强制 fallback。

完成标准：P0 不只给 tag count，还能给出“如果实现 event+transition segment，预计新增可命中的模型数”。
