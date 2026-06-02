# 014 - Model IO Profile Counters

Status: `done`

Date: `2026-06-03`

Code commit: `EVAS dff5e56`

Related scratch logs:

- `/private/tmp/evas-profile-014/inverter_chain.log`
- `/private/tmp/evas-profile-014/clk_div_div8.log`
- `/private/tmp/evas-profile-014/cmp_delay.log`
- `/private/tmp/evas-profile-014/adc_ramp.log`
- `/private/tmp/evas-profile-014/noise_gen.log`

## One-Line Summary

新增 opt-in `EVAS_PROFILE_MODEL_IO=1`，统计 model evaluate 热路径里的 `V(node)` read 和 `<+` output write 调用密度，用数据指导下一步 node-id/Rust lowering。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| `Simulator.run()` | 只能知道 model evaluate 总时间 | 可 opt-in 统计 voltage reads/output writes | 默认无变化 |
| `evas_simulate()` runner | 支持 section/model timing profile | 新增 `evas_profile_model_io` simopt 和 `EVAS_PROFILE_MODEL_IO` 环境变量 | 默认无变化 |
| logging | 无 model IO 调用密度 | profile enabled 时输出 `Model IO counters:` | 只影响 profile log |
| tests | 只有 timing/indexed profile coverage | 新增 engine 和 runner IO profile coverage | 默认无变化 |

## Principle

这一步属于 **诊断 model evaluate 热路径**，不是直接加速。

012 已经显示：

```text
model_evaluate_s 是当前样本中最主要的 model-loop timing
```

013 又证明单个 mapped read/write 的节点解析可以被缓存加速。但是要决定下一步是否继续向 node-id/Rust 迁移，需要知道每个 benchmark 里到底有多少次：

```text
V(node) read
V(out) <+ expr write
```

如果每个 internal step 有大量 read/write，那么把它们从 Python string/dict/helper call 迁到：

```text
node id -> array[index]
```

会更有价值。如果 read/write 很少，而步数很多，那么下一步可能更应该看 event queue、timer 或 step control。

014 的设计是只在 opt-in profile 下安装 probe/write-through hook。默认路径不安装 hook，所以不把诊断计数成本带进正常 EVAS speed path。

## Before / After Evidence

### Validation

Commands run:

```bash
python3 -m pytest tests/test_engine.py::TestSimulator::test_model_io_profile_counts_voltage_reads_and_output_writes tests/test_netlist.py::TestIndexedMigrationHarness::test_evas_simulate_logs_model_io_profile_when_opted_in -q
python3 -m pytest tests/test_engine.py::TestSimulator::test_model_eval_profile_is_explicitly_opted_in tests/test_engine.py::TestSimulator::test_model_io_profile_counts_voltage_reads_and_output_writes tests/test_engine.py::TestSimulator::test_indexed_arrays_build_model_io_plan_without_changing_mapped_output tests/test_netlist.py::TestIndexedMigrationHarness::test_evas_simulate_logs_indexed_arrays_when_opted_in tests/test_netlist.py::TestIndexedMigrationHarness::test_evas_simulate_logs_model_eval_profile_when_opted_in tests/test_netlist.py::TestIndexedMigrationHarness::test_evas_simulate_logs_model_io_profile_when_opted_in -q
python3 -m pytest tests -q
git diff --check
```

Results:

```text
2 passed in 0.45s
6 passed in 0.92s
437 passed in 30.44s
git diff --check: clean
```

### Local Example Profile

Commands:

```bash
mkdir -p /private/tmp/evas-profile-014
EVAS_PROFILE_MODEL_IO=1 python3 -m evas.cli simulate evas/examples/digital_basics/tb_inverter_chain.scs -o /private/tmp/evas-profile-014/inverter_chain -l /private/tmp/evas-profile-014/inverter_chain.log
EVAS_PROFILE_MODEL_IO=1 python3 -m evas.cli simulate evas/examples/clk_div/tb_clk_div_div8.scs -o /private/tmp/evas-profile-014/clk_div_div8 -l /private/tmp/evas-profile-014/clk_div_div8.log
EVAS_PROFILE_MODEL_IO=1 python3 -m evas.cli simulate evas/examples/comparator/tb_cmp_delay.scs -o /private/tmp/evas-profile-014/cmp_delay -l /private/tmp/evas-profile-014/cmp_delay.log
EVAS_PROFILE_MODEL_IO=1 python3 -m evas.cli simulate evas/examples/adc_dac_ideal_4b/tb_adc_dac_ideal_4b_ramp.scs -o /private/tmp/evas-profile-014/adc_ramp -l /private/tmp/evas-profile-014/adc_ramp.log
EVAS_PROFILE_MODEL_IO=1 python3 -m evas.cli simulate evas/examples/noise_gen/tb_noise_gen.scs -o /private/tmp/evas-profile-014/noise_gen -l /private/tmp/evas-profile-014/noise_gen.log
```

Important: these runs have profile enabled and must not be used as paper-facing wall-time evidence.

| Case | Accepted tran steps | Internal steps | Voltage reads | Output writes | Reads / internal step | Writes / internal step | Event-context reads | Read nodes | Write nodes | Cache entries |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `adc_ramp` | 804 | 190401 | 4279965 | 952015 | 22.48 | 5.00 | 180 | 9 | 5 | 17 |
| `clk_div_div8` | 1527 | 61289 | 61290 | 61291 | 1.00 | 1.00 | 0 | 1 | 1 | 2 |
| `cmp_delay` | 1814 | 232859 | 1164397 | 698583 | 5.00 | 3.00 | 96 | 5 | 3 | 9 |
| `inverter_chain` | 373 | 46124 | 184504 | 184504 | 4.00 | 4.00 | 0 | 4 | 4 | 8 |
| `noise_gen` | 50937 | 50937 | 50939 | 50939 | 1.00 | 1.00 | 0 | 1 | 1 | 2 |

Interpretation:

- `adc_ramp` is read-heavy: about `22.48` voltage reads per internal step.
- `cmp_delay` is also meaningful: about `5` reads and `3` writes per internal step.
- `inverter_chain` has balanced read/write density: about `4 + 4` per internal step.
- Event-context reads are small in these examples; ordinary non-event reads dominate.
- This supports continuing toward ordinary branch access/output write node-id lowering before attempting a global event queue rewrite.

## Functional Safety

- Default backend changed: `no`
- Default hooks installed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Profile-on wall usable for speed claim: `no`
- Accuracy impact: `none expected`; focused tests compare default/profile waveform equality

## Learning Notes

### 什么是调用密度？

如果一个仿真有：

```text
internal steps = 190401
voltage reads = 4279965
```

那么每个内部 step 平均大约：

```text
4279965 / 190401 = 22.48 reads/step
```

这说明即使 accepted tran steps 看起来不多，模型内部仍然在高频重复执行 `V(node)`。

### 为什么这会指导 Rust 化？

Python 当前执行一次普通 read 大致包含：

```text
Python method call
local node string
node_map/cache lookup
external node string
dict lookup
float object handling
```

Rust/node-id 后可以把普通 read 变成：

```text
values[node_id]
```

如果每个 internal step 有 20 多次 read，这种替换会累积成真实的 per-step 成本下降。

### 为什么 event-context reads 要单独看？

event body 中的 `V(node)` 可能表示 crossing time 上的插值值，不是当前 step array 里的普通值。014 的样本里 event-context reads 很少，所以现阶段优先迁移普通 non-event read 更合理；event read 可以保留原插值路径，后续单独设计。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| profile hook 被误用于默认速度 claim | 报告引用 profile-on wall time | 把 014 标为 diagnostic-only，不使用 profile wall |
| profile hook 和 indexed hooks 冲突 | indexed/profile focused tests 失败 | 回退 EVAS commit `dff5e56` |
| counter 统计口径误读 | 把 accepted steps 当作内部执行步数 | 同时报告 `accepted tran steps` 和 `steps_total` |
| 样本不代表 vaBench release | release profile 调用密度不同 | 用 014 工具对 release rows 再跑一轮 profile |

## Next Step

下一篇审计文档建议：

- `015-static-branch-access-node-id-plan.md`：把非数组、非 event 的静态 `V(node)`/`V(out)<+` lowering 边界整理成 node-id plan，优先做不改语义的 IR/plan，再决定是否进入 Python array-backed helper 或 Rust native evaluator。
