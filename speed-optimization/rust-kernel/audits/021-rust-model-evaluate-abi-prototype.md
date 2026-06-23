# 021 - Rust Model Evaluate ABI Prototype

Status: `done`

Date: `2026-06-03`

Code commit: `EVAS 0263986`

Related paths:

- `EVAS/prototypes/rust-kernel-smoke/src/main.rs`
- `EVAS/prototypes/rust-kernel-smoke/run_kernel_benchmarks.py`
- `EVAS/prototypes/rust-kernel-smoke/README.md`

## One-Line Summary

新增一个最小 Rust `model-abi` kernel，用 node id、scalar state id 和 compact parameter struct 驱动 native `Vec<f64>` evaluate loop，验证 017-020 准备的数据布局可以脱离 Python dict/string 热路径运行。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| Rust smoke prototype | 只有 measurement indexed、PFD fixed-step 和 PFD event-queue toy kernels | 新增 `--kernel model-abi` | 只影响 prototype |
| model evaluate ABI | 没有 Rust 侧 model read/write/state 接口 | 新增 `ModelEvalAbi`，包含 read node ids、write node ids、scalar state ids、参数 | 默认 EVAS runtime 不变 |
| ABI failure path | toy kernel 没有 layout 错误类型 | 新增 `AbiError`，覆盖缺 read/write/state slot 和越界 node/state | 只影响 Rust tests |
| benchmark runner | 不记录 Rust model ABI 结果 | 新增 `rust_model_abi` 配置和相对 Python dict/indexed 的 speedup 字段 | 只影响 prototype JSON |

## Principle

这个改动属于 **降低每步成本** 的 Rust 化前置验证。

EVAS 当前 Python model evaluate 热路径里常见的访问方式是：

```text
V(vin)        -> Python helper -> string node name -> dict lookup
self.state[x] -> Python string key -> dict lookup
V(vout) <+ y  -> Python helper -> string node name -> dict write
```

017-020 的前置改造已经把这些对象路径拆成 metadata：

```text
read_node_ids        = [vin_id]
write_node_ids       = [vout_id]
scalar_state_ids     = [state_id]
dynamic/event/state  = separated metadata
```

021 用 Rust prototype 验证最核心的形状：

```text
input:  values[node_id], scalar_state[state_id], compact params
update: scalar_state[state_id] = f(values[node_id], old_state, params)
output: values[out_node_id] = scalar_state[state_id] * gain + bias
```

这一步不是把 EVAS runtime 切到 Rust，而是证明 Rust 侧可以用连续数组和整数 id 完成 model evaluate。真正接入生产 runtime 时，下一步必须先解决 Python/Rust batch 边界，否则如果每个 model 每个 step 都跨一次 FFI，边界成本会吃掉 Rust hot loop 收益。

## Before / After Evidence

| Metric | Before | After | Interpretation |
|---|---:|---:|---|
| default EVAS runtime | Python generated model code | unchanged | 021 不改变默认仿真 |
| Rust model ABI availability | none | `--kernel model-abi` | 新增 prototype-only kernel |
| model ABI smoke wall | n/a | `0.078045 s` for 200000 steps, 64 models | 本地 hot loop 方向可行 |
| checker/result parity | n/a | Rust tests deterministic | 只验证 prototype determinism，不是 Spectre parity |

Validation commands:

```bash
cargo test --release
cargo run --release -- --kernel model-abi --steps 200000 --models 64 --record-stride 16
python3 run_kernel_benchmarks.py --repeats 1 --steps 1000 --pfd-steps 1000 --models 4 --record-stride 8 --output /private/tmp/evas_rust_kernel_abi_smoke_20260603.json
git diff --check
```

Important output:

```text
cargo test --release: 5 passed; 0 failed
engine=rust_indexed kernel=model-abi requested_steps=200000 processed_steps=200000 models=64 record_stride=16 elapsed_s=0.078045 events=0 checksum=5398.789823966 err_acc=71.115918716
runner smoke: rust_model_abi processed_steps=1000 events=0 checksum=55.072084181 elapsed_s=0.000020
git diff --check: clean
```

Interpretation:

- `model-abi` 证明 node/state id ABI 可以驱动 Rust `Vec<f64>` evaluate loop。
- 这个数字只能说明 local prototype hot loop 很快，不能声明 EVAS 已经快于 Spectre AX。
- 021 没有运行 vaBench release full rerun，也没有做 Spectre parity，因此不能作为 paper-facing speed/accuracy claim。

## Functional Safety

- Default backend changed: `no`
- Default generated runtime code changed: `no`
- Runtime state storage changed: `no`
- Event interpolation changed: `no`
- Dynamic bus runtime changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`
- Accuracy impact: `none expected`; production EVAS runtime is untouched

## Learning Notes

### 什么是 ABI？

ABI 可以理解成两边代码约定好的“接口形状”。这里的两边是 Python EVAS 和未来 Rust kernel。

Python 不应该把一堆字符串、dict、复杂对象逐个传给 Rust，而应该提前整理成简单数组和编号：

```text
node_values:       [v0, v1, v2, ...]
scalar_state:      [s0, s1, s2, ...]
model.read_ids:    [3, 5]
model.write_ids:   [8]
model.state_ids:   [0]
model.parameters:  {alpha, gain, bias}
```

Rust 只按整数下标读写数组。这样做快，是因为 CPU 更擅长处理连续内存和整数下标，而不是 Python object、字符串 hash 和 dict indirection。

### 为什么不能每次 evaluate 都从 Python 调一次 Rust？

跨语言调用本身有固定成本。若每个 model 每个 step 都调用一次 Rust：

```text
for step:
  for model:
    call_rust_one_model(...)
```

那么 Rust 内部虽然快，但大量小调用会浪费在边界上。更合理的方向是 batch：

```text
call_rust_many_steps_many_models(...)
```

也就是一次传入 node/state arrays、model ABI table、step window，让 Rust 在内部完成一批 evaluate，再把必要结果交回 Python。

### 021 和 017-020 是什么关系？

- 017 让静态 branch read/write 能直接用 node id。
- 018 区分 event trigger 和 event body，避免 Rust 化时破坏 crossing-time interpolation。
- 019 暴露 dynamic bus access metadata，为 bus base+offset lowering 做准备。
- 020 暴露 scalar/array state layout。
- 021 把这些思想压缩成一个最小 Rust prototype，验证 node/state id + compact params 的 evaluate loop 能工作。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| 把 prototype benchmark 误写成 release speed claim | 报告中出现 EVAS 已经快于 AX 的直接结论 | 保留 021 claim boundary，回到同片 release timing |
| Rust ABI 过早接入 production runtime | vaBench parity 或 examples capability 退化 | 回退 EVAS commit `0263986` 或保持 prototype-only |
| 每 model 每 step FFI 调用过多 | Rust 接入后 wall time 没有下降甚至变慢 | 先做 batch ABI plan，再做 runtime integration |
| ABI 忽略 dynamic bus/event/state edge cases | dynamic bus、event interpolation、integer state regressions | 继续沿 018-020 metadata 边界逐类 lowering |

## Next Step

下一篇建议做：

- `022-rust-ffi-batch-evaluate-plan.md`
- `023-dynamic-bus-runtime-lowering.md`

022 应先设计 Python/Rust batch evaluate 边界，避免 per-model FFI 小调用。023 可以修复和降低 019 记录的 dynamic bus runtime/codegen 风险，为更多 real-row model evaluate 进入 Rust 做准备。
