# 046 - Fixed-Index State Array IR

Status: `done`

Date: `2026-06-04`

Code commit: `pending`

Related reports:

- `speed-optimization/reports/rust_fixed_array_topwall10_20260604.json`
- `speed-optimization/reports/rust_fixed_array_topwall10_20260604.md`

## One-Line Summary

把 `arr[常量]` 形式的 state array 读写纳入 Rust static-linear evaluate IR，先解锁固定数组元素模型，不处理运行时动态下标。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| Compiler IR | static-linear evaluate IR 只接受 scalar state；`arr[i]` 一律拒绝 | `arr[0]`、`arr[N-1]` 这类固定整数下标可作为 `SOURCE_STATE` / `TARGET_STATE` | 默认 backend 行为不变 |
| Indexed state storage | scalar state 和 array sidecar 分开；Rust state buffer 只含 scalar | 固定数组元素也分配到同一个 `state_values` 扁平槽位，例如 `tap[1]` | CSV/checker/strobe 不变 |
| Python fallback | `_array_get/_array_set` 只读写 `self.arrays` 和 array sidecar | 同步读写 array sidecar 和扁平 state slot，保证 Rust 更新后 Python 也能看到 | 功能语义不变 |
| Rejection audit | 固定数组和动态数组都报 `assignment_array_target` / `expr_array_access` | 固定数组不再报拒绝；动态下标额外记录 `*_dynamic_array_index` | 后续 top-wall blocker 更清晰 |

## Principle

这是 **降低每步成本** 的前置 coverage 改造，不是直接 speed claim。

原来的 Rust static-linear ABI 已经有一个 `state_values: Vec<f64>`，但它只装 scalar state，例如 `sample`。很多真实 Verilog-A 模型会使用小数组，例如 `tap[0]`、`hist[1]`、`code[3]`。如果这些数组元素仍然保存在 Python `dict`/array sidecar 里，Rust evaluate 就找不到对应 state id，整个模型只能 fallback 到 Python。

这次不新增 Rust ABI，而是把固定数组元素扁平化成普通 state slot：

```text
sample      -> state_values[0]
tap[0]      -> state_values[1]
tap[1]      -> state_values[2]
```

这样 Rust 内核仍然执行同一个数组循环：

```text
target_slot = bias + gain0 * source_slot0 + gain1 * source_slot1
```

它快的原因不是 `tap[1]` 这个名字本身，而是运行时不再需要 Python dict lookup、字符串 key lookup、`_array_get()` 调用和 Python object 装箱。固定下标可以安全扁平化；动态下标 `tap[i]` 还不行，因为 `i` 是运行时状态，每一步可能变化，需要后续单独的 dynamic array/index IR。

## Before / After Evidence

| Metric | Before | After | Interpretation |
|---|---:|---:|---|
| fixed-index array unit model Rust coverage | rejected | 3 static-linear ops planned | coverage 增加 |
| dynamic-index array model Rust coverage | rejected | rejected | 保守边界保持 |
| checker/result parity | targeted tests pass | targeted tests pass | 功能不变 |
| top-wall 10 Python fast total wall | 18.541s in 045 rerun | 18.268s | run-to-run noise; not a claim |
| top-wall 10 Rust-required total wall | 21.362s in 045 rerun | 21.233s | still slower than Python fast |
| top-wall Rust planned ops/calls | 6 ops / 32472 calls on gain-extraction rows | unchanged | fixed arrays did not unlock new top-wall models |

本轮不能声明 EVAS 速度提升。top-wall 10 诊断显示 10/10 PASS，但 fixed-index array IR 没有解锁新的真实 top-wall Rust 模型。

Top-wall 10 EVAS-only mode summary:

| Mode | PASS | Total wall s |
|---|---:|---:|
| `profile_fast_skip_source_error_control` | 10/10 | 18.268 |
| `profile_fast_rust_static` | 10/10 | 21.233 |

Rust-required 仍然比 Python fast 慢。真实 top-wall 里只有 gain-extraction 两行仍有 2 个小 Rust candidates、6 ops、32472 calls；这是 Python/Rust 边界开销大于内核收益的坏区间。

Aggregate rejection counts after 046:

| Reason | Count | Interpretation |
|---|---:|---|
| `expr_function_transition` | 47 | transition 仍是主要 blocker |
| `event_statement` | 27 | event/timer/cross 仍阻塞完整 Rust evaluate |
| `assignment_self_dependent_state` | 46 | recurrence/state update 还不能安全 lowering |
| `assignment_array_target` | 8 | 仍有数组 target blocker |
| `expr_array_access` | 4 | 仍有数组 read blocker |
| `assignment_dynamic_array_index` | 8 | 数组 blocker 主要是动态下标，不是固定下标 |
| `expr_dynamic_array_index` | 4 | 读路径同样需要 dynamic array/index IR |

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`

## Validation

Commands run:

```bash
PYTHONPATH=EVAS python3 -m pytest \
  EVAS/tests/test_engine.py::TestSimulator::test_rust_static_eval_handles_simple_state_linear_model \
  EVAS/tests/test_engine.py::TestSimulator::test_rust_static_eval_handles_fixed_index_state_array_model \
  EVAS/tests/test_engine.py::TestSimulator::test_rust_static_eval_rejects_dynamic_state_array_index \
  EVAS/tests/test_engine.py::TestSimulator::test_rust_static_eval_handles_integer_state_linear_model -q
```

Result:

```text
4 passed in 1.37s
```

Commands run:

```bash
PYTHONPATH=EVAS python3 -m pytest \
  EVAS/tests/test_engine.py::TestSimulator::test_rust_static_eval_matches_default_for_static_affine_model \
  EVAS/tests/test_engine.py::TestSimulator::test_rust_static_eval_handles_fixed_index_state_array_model \
  EVAS/tests/test_engine.py::TestSimulator::test_rust_static_eval_handles_initial_step_and_conditional_state_model \
  EVAS/tests/test_engine.py::TestSimulator::test_rust_transition_shadow_matches_ordered_state_target_segment \
  EVAS/tests/test_indexed_backend.py::test_indexed_state_storage_mirrors_scalar_and_array_writes \
  EVAS/tests/test_indexed_backend.py::test_compiled_model_records_static_linear_evaluate_ir_for_differential_model \
  EVAS/tests/test_indexed_backend.py::test_static_linear_evaluate_ir_executes_state_assignment_then_output -q
```

Result:

```text
7 passed in 1.96s
```

Commands run:

```bash
PYTHONPATH=EVAS python3 -m pytest EVAS/tests -q
```

Result:

```text
516 passed in 35.21s
```

Targeted subset:

```bash
PYTHONPATH=EVAS python3 -m pytest \
  EVAS/tests/test_engine.py \
  EVAS/tests/test_indexed_backend.py \
  EVAS/tests/test_rust_backend.py -q
```

Result:

```text
271 passed in 4.91s
```

Remote on `thu-sui` with Linux Rust backend:

```bash
cd /home/jinzhihong/vaevas-speed-clean-current-20260604-0034
PYTHONPATH=EVAS python3 -m pytest \
  EVAS/tests/test_engine.py::TestSimulator::test_rust_static_eval_handles_simple_state_linear_model \
  EVAS/tests/test_engine.py::TestSimulator::test_rust_static_eval_handles_fixed_index_state_array_model \
  EVAS/tests/test_engine.py::TestSimulator::test_rust_static_eval_rejects_dynamic_state_array_index \
  EVAS/tests/test_engine.py::TestSimulator::test_rust_static_eval_handles_integer_state_linear_model -q
```

Result:

```text
4 passed in 2.77s
```

Top-wall 10 EVAS-only diagnostic on `thu-sui`:

```bash
cd /home/jinzhihong/vaevas-speed-clean-current-20260604-0034/behavioral-veriloga-eval
PYTHONPATH=runners:../EVAS python3 runners/run_vabench_release_evas_speed_experiment.py \
  --speed-artifact speed-optimization/reports/topwall10_speed_rows_from_fourway_20260604.json \
  --suite top-wall \
  --limit 10 \
  --mode profile_fast_skip_source_error_control \
  --mode profile_fast_rust_static \
  --timeout-s 900 \
  --jobs 1 \
  --output-root results/rust-fixed-array-topwall10-20260604 \
  --report-json speed-optimization/reports/rust_fixed_array_topwall10_20260604.json \
  --report-md speed-optimization/reports/rust_fixed_array_topwall10_20260604.md
```

Result:

```text
wrote EVAS speed experiment: rows=10; modes=profile_fast_skip_source_error_control,profile_fast_rust_static
```

## Learning Notes

### 什么是“固定下标数组”？

`tap[0]`、`tap[1]`、`tap[N-1]` 这种下标在编译期就能算出来，叫固定下标。`tap[i]` 的 `i` 是仿真过程中变化的状态，叫动态下标。

固定下标可以像普通变量一样编号：

```text
tap[0] -> 1
tap[1] -> 2
```

动态下标不能这么做，因为每一步访问哪个元素要等运行时才知道。

### 为什么这对 Rust 化重要？

Rust 最擅长的是连续数组循环：

```text
for op in ops {
    state[target] = bias + sum(gain * state[source])
}
```

Python 当前很多路径是字典和对象：

```text
self.arrays["tap"][1]
self.state["sample"]
```

字典适合写代码和动态行为，但在每步几十万次的仿真循环里很贵。把 `tap[1]` 变成一个整数 slot 后，Rust/Python 都可以直接访问 `state_values[slot]`。

### 为什么不直接支持所有数组？

因为 `tap[i]` 的 `i` 可能来自 `cross` event、timer、case、循环或前一步状态。错误地把 `tap[i]` 当成 `tap[0]` 会改变仿真结果。现阶段只接受能严格证明为固定整数的下标；剩下的动态数组要等后续 dynamic array/index IR。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| 固定数组 slot 写回错误 | Rust path 波形对，但最终 `model.arrays[...]` 不一致 | 回退 `CompiledModel._set_indexed_state_storage()` / `_commit_indexed_state_storage()` 的 array slot 映射 |
| 动态数组被误判成固定数组 | `tap[i]` 模型进入 Rust static-linear ops | 回退 `_evaluate_ir_static_array_index*()`，只保留 `NumberLiteral` |
| array sidecar 旧路径被破坏 | `test_indexed_state_storage_mirrors_scalar_and_array_writes` 失败 | 回退 `_array_get/_array_set()` 对扁平 slot 的读写 |

## Next Step

- `047 - Dynamic State Array Index IR Audit`

046 的 top-wall rerun 已经说明固定数组不是当前 top-wall 主瓶颈。后续不要继续做固定数组小修，应转向：

1. dynamic array/index IR，覆盖 `arr[i]` 读写和 loop index；
2. `transition()` production path，而不只是 shadow/parity；
3. event/timer/cross queue Rust/array 化；
4. self-dependent state recurrence IR。
