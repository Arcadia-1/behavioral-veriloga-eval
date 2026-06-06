# 108 - Rust-Owned Simulation Loop First

Status: `active`

Date: `2026-06-06`

Code commit: `pending`

Related reports:

- `105-evas2-strict-rust-engine.md`
- `106-evas2-event-transition-core-strict-production.md`
- `107-evas2-native-scheduler-sparse-record.md`
- `RUST_NEGATIVE_ATTEMPT_STOPLIST_20260605.md`

## One-Line Summary

EVAS2 的主线从“继续堆窄 whole-segment fastpath”纠正为“先迁移仿真主循环和完整 Verilog-A 行为语义”：Python 只负责 parse/lower/runner 兼容，Rust 拥有 transient scheduler、source、event、evaluate、transition、breakpoint、record 和 final state。

## Why This Reset Is Needed

107 证明了一个重要事实：当 scheduler、event body、transition 和 record 被合成一次 Rust trace ABI 后，microbench 可以从 Python per-point loop 的 `0.389472s` 降到 `0.007946s`，约 `49.02x` faster than 106。

但是 107 的 release 覆盖面为零：

| Corpus | `.va` files scanned | 107 static hits |
|---|---:|---:|
| `benchmark-vabench-release-v1/tasks` | `357` | `0` |
| historical `tasks` | `271` | `0` |

这说明继续扩展 W1b 这类手写 shape fastpath 只会得到更多局部加速证据，不能自然变成全量 EVAS2。正确方向是把 Python EVAS 已经拥有的完整仿真语义 lowering 成 Rust 可执行 program，然后让 Rust 拥有主循环。

## Current Wrong Shape

当前多数 Rust 改造仍然是 Python-owned loop：

```text
Python while time < tstop:
    decide dt
    scan source/model/bound_step breakpoint
    copy prev node dict / indexed array
    update source voltages
    call model._prepare_step()
    call model.evaluate() or tiny Rust kernel
    call post_update_events()
    scan err_ratio
    append record point
```

即使某些局部函数进了 Rust，只要主循环仍由 Python 每步调度，就会继续支付：

- Python object/dict/string lookup；
- 每步 Python/Rust FFI；
- node/state packing 和 sync；
- Python list append record；
- Python event/timer/breakpoint scan；
- Python lifecycle call overhead。

104 的负优化和 107 的正收益都指向同一条原则：**Rust 必须拿到足够大的仿真段，而不是每步被 Python 调用。**

## Target Shape

EVAS2 应该变成 Rust-owned transient engine：

```text
Python:
    parse Verilog-A / Spectre netlist
    compile model AST to RustSimProgram IR
    map node/state/param/source/record ids
    call rust_run_transient(program, run_options)
    convert Rust trace to SimResult / CSV / checker input

Rust:
    own time loop
    own source waveform evaluation and source breakpoints
    own event queue: initial_step, cross, above, timer, final_step
    own event body writes: state, arrays, outputs, timers, files where supported
    own continuous evaluate and contribution ordering
    own transition state, transition breakpoints, output writes
    own bound_step and adaptive/error-ratio scans
    own sparse record buffers
    return final node/state/output/trace/stats
```

Python can remain the front-end and benchmark harness. It should not remain the per-step simulator scheduler for EVAS2 strict mode.

## Required RustSimProgram Boundary

The first implementation target is not another model-specific ABI. It is a typed program contract:

| Program section | What Rust must receive | Why it belongs in Rust |
|---|---|---|
| Node layout | node names, external mapping, source/output/record ids | removes per-step dict/string lookup |
| State layout | scalar, integer, array ranges, initial values | removes Python state dict/list sync |
| Parameters | typed scalar parameter array and resolved constants | avoids Python scalar evaluation inside loop |
| Sources | dc, pulse, sine, pwl metadata and breakpoint rules | source values and source breakpoints drive dt |
| Analog statements | ordered continuous evaluate, event statements, contribution statements | preserves Verilog-A source order |
| Event due | initial_step, cross, above, timer programs | event scheduler must be native, not helper-only |
| Event body | state/array/output/timer/file write programs | event semantics must move with event due |
| Transition | target expression, delay/rise/fall, state machine | transition state and breakpoints define dt |
| Bound step | `$bound_step` expressions and ownership | timestep control cannot stay Python-only |
| Record | required signal ids, sparse record cadence | E2E speed depends on avoiding Python append/copy |

Unsupported features must be explicit compile-time rejection reasons in EVAS2 strict mode, not silent Python fallback.

## Migration Order

| Step | Scope | Proof gate |
|---|---|---|
| 108a | Define `RustSimProgram` schema and release coverage reporter | every release row gets `rust_program_ok` or exact rejection reason |
| 108b | Build Rust main-loop skeleton for sources + record + no-model passthrough | parity against Python source-only simulations |
| 108c | Lower continuous evaluate + simple state/output writes into Rust program | parity on static and stateful non-event models |
| 108d | Lower event queue with `initial_step/cross/above/timer` plus event body writes | parity on event-heavy release rows |
| 108e | Move transition and breakpoint ownership into the same Rust loop | no Python model breakpoint scan for covered rows |
| 108f | Move adaptive err-ratio, `$bound_step`, final_step, sparse record into Rust | strict EVAS2 can run covered benchmark rows end-to-end |
| 108g | Run release-wide coverage and speed table | claim only rows where EVAS2 strict is Rust-owned |

## What Not To Do Next

- Do not add more hand-written benchmark-name fastpaths.
- Do not add another per-step Rust FFI helper and call it from the Python loop.
- Do not count Python fallback as EVAS2 coverage.
- Do not report microbench speedup as benchmark speedup.
- Do not optimize checker/CSV before the Rust main loop coverage gate, except for regression safety.

## Claim Gate

Until `RustSimProgram` can run real release rows under strict mode:

- safe to say: 107 proves the performance mechanism of coarse Rust batching;
- not safe to say: EVAS2 supports release benchmark simulation;
- not safe to say: EVAS2 is faster than Spectre AX;
- not safe to say: EVAS has been fully Rustified.

The next meaningful percentage is not “how many primitives exist in Rust”; it is:

```text
release rows where Python EVAS and Rust EVAS2 strict produce checker-equivalent results
/
release rows that Python EVAS can currently simulate
```

That is the only percentage that matches the user-facing goal of “EVAS2 can run the benchmark.”

## 2026-06-06 Implementation Update

本轮把 108 从 source/record/static-linear 主循环推进到第一段 **event queue + event body + transition/breakpoint** 的统一 RustSimProgram production 子集。它不是全量 Rust EVAS2，但已经不再只是 schema 留口。

| 108 item | 当前状态 | 已验证证据 | 还缺什么 |
|---|---|---|---|
| 108a `RustSimProgram` typed schema | done for `node/state/param/source/event/body/transition/record`；新增 `body_stmt_ops/body_expr_ops/events/transitions/params` | `evas/simulator/rust_program.py` + `evas/simulator/rust_backend.py` ABI | array state、dynamic bus、file/task side effect、full adaptive metadata 仍需扩 schema |
| 108b source + record + no-model Rust loop | done | source-only strict parity 回归仍通过 | adaptive source err-ratio 未迁移；source-only parity 仍用 `skip_source_error_control=True` 隔离 108b |
| 108c continuous evaluate / state write / output write | partial production | static-linear evaluate/state/output 子集在 Rust loop 中执行 | 自反馈 state update、非线性函数、数组 state、复杂控制流还不能 lowering |
| 108d event queue + event body | partial production | 新增 strict full-model parity：`initial_step` + `cross()` due + body state write 在 RustSimProgram 执行，`generic_executor_runs == 0` | `timer()` 暂不进入这个新入口；full event ordering、post-update queue、复杂 body/side effect 未迁移 |
| 108e transition + breakpoint ownership | partial production | 同一 strict test 中 `transition()` target/output/breakpoint 由 RustSimProgram 执行，`transition_breakpoints > 0` | whole-segment transition batch、mixed timer/cross queue、复杂 target/control flow 未迁移 |
| 108f `$bound_step` / adaptive / final_step / sparse record | not done | 无 | 当前 RustSimProgram 不拥有 err-ratio、`$bound_step`、`final_step`、sparse trace 全链路 |
| 108g release-wide strict run + speed table | coverage audit only | release static smoke 可构造 RustSimProgram candidates，但 coverage reporter 仍需刷新 event/transition 细分字段 | 不能生成 benchmark speed table；还没有 release row 级 strict Rust EVAS2 e2e gate |

### Implemented Runtime Boundary

新增 Rust-owned loop 当前覆盖：

```text
Rust:
    initialize node/state arrays
    write source values at t=0
    run initial_step event bodies
    run continuous static-linear evaluate ops
    apply transition target/output state
    record initial point
    while time < tstop:
        clamp dt by tstep/maxstep/tstop
        clamp source pulse/PWL breakpoints
        clamp transition breakpoints
        clamp record_step
        write source values
        run cross/above event due checks for supported events
        execute supported event body write-set
        run continuous static-linear evaluate ops
        apply transition target/output state
        record selected node ids
    return trace + final node/state arrays + event/transition stats
```

Python 仍负责 parse/lower/runner，并且只在 strict EVAS2 入口前做一次 program build。覆盖成功后，Python 不再逐步调用 `model.evaluate()` 或通用 event body executor。

### Lowering Rule

这次不是按 benchmark 名称或端口名命中 fastpath，而是从 compiled model 的 `_module_ast` 做语义/dataflow lowering：

- `EventStatementIR` -> event due program + body statement program；
- body expression/local state/param/node slot -> global RustSimProgram slot；
- `ContributionIR` with `transition(...)` -> transition target/delay/rise/fall expression segment；
- source/record/continuous static-linear ops 与 event/transition 在同一 Rust call 内执行。

如果模型含 child model、state array、`$bound_step`、post-update event、无法编码的 body stmt 或 transition expression，strict RustSimProgram 会显式 reject，而不是静默混入 Python fallback。

### Timer Safety Decision

本轮曾尝试把 generic `timer()` 也放进新 event queue，但完整 `tests/test_engine.py` 暴露了 timer-static-linear 回归的时间网格差异。当前处理是：

- `timer()` 不进入新的 generic event-transition RustSimProgram；
- 已验证的旧 timer-static-linear whole-segment Rust 路径继续保留；
- generic RustSimProgram 对 timer 返回 `timer_event_queue_not_lowered`。

这是为了避免把一个看似更“全量”的入口变成负迁移。timer 的正确做法是后续把 existing timer-static-linear 语义并入统一 scheduler，并用相同 trace grid/parity gate 证明。

### Coverage Smoke Caveat

当前 `rust_coverage.py` 的 `rust_sim_program_candidates` 只是“能静态构造 RustSimProgram”的模型级审计，不是 release benchmark row 已经跑通的证明；它也还没有把 event count、body ops、transition count 纳入明细字段。因此本轮不把 coverage 数字写成最终覆盖率或速度 claim。

下一步需要刷新 coverage schema：

| Field to add | Why |
|---|---|
| `rust_sim_program_event_count` | 区分 source/static-linear model 和 event model |
| `rust_sim_program_body_stmt_ops` / `body_expr_ops` | 量化 event body 是否真正 lowering |
| `rust_sim_program_transition_count` | 量化 transition/breakpoint 是否进入 Rust loop |
| `rust_sim_program_timer_rejected` | 防止 timer 被误读为已经统一迁移 |
| row-level strict run result | coverage claim 必须以完整 benchmark row checker parity 为准 |

### Current Remaining Blockers

| Blocker class | Meaning |
|---|---|
| `timer_event_queue_not_lowered` | generic RustSimProgram 还没有拥有 timer grid/order；旧专用 timer path 保留 |
| `post_update_not_lowered` | post-update event semantics remain Python-owned |
| `bound_step_not_lowered` | `$bound_step` remains outside the RustSimProgram scheduler |
| arrays / dynamic bus | body/state/output write-set 还不能覆盖数组和动态节点索引 |
| complex control flow / nonlinear expr | 当前 BodyExpr/Stmt 子集还不是完整 Verilog-A interpreter |
| row-level runner integration | 还没有 release-wide strict Rust EVAS2 e2e checker/speed 表 |

### Verification

EVAS repo checks run locally:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/evas_pycache_event_transition python3 -m py_compile \
  EVAS/evas/simulator/rust_program.py \
  EVAS/evas/simulator/rust_backend.py \
  EVAS/evas/simulator/engine.py

cd EVAS/evas/rust_core && cargo build --release

PYTHONPATH=/Users/bucketsran/Documents/TsingProject/vaEvas/EVAS \
python3 -m pytest EVAS/tests/test_engine.py -q \
  -k 'rust_sim_program or event_transition_strict'

PYTHONPATH=/Users/bucketsran/Documents/TsingProject/vaEvas/EVAS \
python3 -m pytest EVAS/tests/test_engine.py -q
```

Observed:

- Python compile check: pass
- Rust release build: pass
- targeted pytest: `6 passed, 250 deselected`
- full engine pytest: `256 passed`

`cargo fmt` was not run because the local stable toolchain is missing `rustfmt`.
