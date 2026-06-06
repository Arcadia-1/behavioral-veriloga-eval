# 102 Compiler-Visible Event/Transition Plan Metadata

Status: diagnostic plumbing, not production speed evidence.

## 这一步改了什么

101 的 source-order planner 还主要服务于 release audit：audit 脚本重新解析 `.va`，再判断 event/output/transition segment 是否具备 Rust lowering 形状。

102 把这个判断前移到 `compile_module()`：每个生成的 `CompiledModel` class 现在都会带上 `_event_transition_plan_*` metadata。这样后续 engine 可以直接根据模型语义决定是否 opt-in Rust segment，而不是按 task name、module name 或端口名写 fastpath。

## 修改位置

- `EVAS/evas/simulator/event_transition_plan.py`
  - 将三个 profile support set 移到 planner 模块，作为唯一口径：
    - `event_transition_core`
    - `event_transition_ordered_v1`
    - `event_transition_with_side_effect_boundary`
- `EVAS/evas/simulator/backend.py`
  - `CompiledModel` 增加 `_event_transition_plan_*` class attributes。
  - `CodeGenerator.generate()` 调用 `_collect_event_transition_plan_metadata(...)`。
  - compile 阶段把 planner summary 写入模型类。
- `EVAS/evas/simulator/rust_coverage.py`
  - audit row 改成读取 compiler-visible class metadata，而不是重新做一份 planner 逻辑。
- `EVAS/evas/simulator/engine.py`
  - 每次 `Simulator.run()` 聚合 event-transition plan stats：
    - core / ordered-v1 / side-effect candidate model count；
    - event statement / due trigger / transition / output-write count。
- `EVAS/tests/test_engine.py`
  - 增加 class metadata 与 engine perf stats regression。

## 为什么这一步重要

这一步回答了用户关心的“是不是根据具体电路决定怎么跑 Rust 内核”。

现在的路径变成：

```text
Verilog-A model
  -> parser AST
  -> compiler lowering / planner
  -> CompiledModel._event_transition_plan_profiles
  -> engine 读取 metadata，后续才能选择 Rust runtime
```

也就是说，后续选择 Rust 的依据是行为语义和数据流，而不是模型名字。端口名变化没有关系，因为 planner 使用的是 node/state/parameter slot。

## 全量 release 数字

命令：

```bash
PYTHONPATH=EVAS python3 EVAS/prototypes/audit_098_current_rust_coverage.py \
  --json-out /private/tmp/evas_rust_coverage_102_compiler_metadata.json
```

结果与 101 保持一致，说明 compiler metadata 没有改变 planner 口径：

| profile | compiler-visible planner candidates |
| --- | ---: |
| `event_transition_core` | 231 / 348 |
| `event_transition_ordered_v1` | 239 / 348 |
| `event_transition_with_side_effect_boundary` | 288 / 348 |

主要 blocker 仍然是：

| profile | rejection summary |
| --- | --- |
| `event_transition_core` | `unsupported_tags` 93, `event_due_unencodable` 14, `event_after_continuous_statement` 10 |
| `event_transition_ordered_v1` | `unsupported_tags` 80, `event_after_continuous_statement` 15, `event_due_unencodable` 14 |
| `event_transition_with_side_effect_boundary` | `event_after_continuous_statement` 34, `event_due_unencodable` 16, `unsupported_tags` 10 |

## 当前仍不能 claim 什么

- 不能 claim 全量 Rust 化。
- 不能 claim EVAS 因 102 变快。
- 不能 claim 这些 231/239/288 rows 已经 production Rust 执行。

102 只是把“哪些模型适合接 Rust runtime”的判断变成 compiler/engine 可见 metadata。下一步才是对 `event_transition_core` 做 shadow parity 和 opt-in production gate。

## 下一步

1. 用 `_event_transition_plan_profiles` 作为 gate，构建 `rust_event_transition_shadow` 选项。
2. 先只接 `event_transition_core`，对 engine 中 Python result 与 Rust shadow result 做 per-step parity。
3. shadow pass 后再做 opt-in production，默认仍 off。
4. 同时补 `event_after_continuous_statement` 的 multi-phase runtime 和 `event_due_unencodable` 的 dynamic timer due。

## 验证

```bash
PYTHONPYCACHEPREFIX=/private/tmp/evas_pycache_102 python3 -m py_compile \
  EVAS/evas/simulator/event_transition_plan.py \
  EVAS/evas/simulator/rust_coverage.py \
  EVAS/evas/simulator/backend.py \
  EVAS/evas/simulator/engine.py \
  EVAS/prototypes/audit_098_current_rust_coverage.py

PYTHONPATH=EVAS python3 -m pytest \
  EVAS/tests/test_engine.py \
  -k "current_rust_coverage or event_transition_plan or body_ir or rust_coverage" -q

PYTHONPATH=EVAS python3 -m pytest \
  EVAS/tests/test_engine.py \
  -k "rust or body_ir or event_due or analog_block or transition_contribution or event_transition_plan" -q
```

结果：

- Targeted tests: `4 passed, 243 deselected`。
- Broader Rust/094 subset: `48 passed, 199 deselected`。
