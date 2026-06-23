# 023 - Dynamic Bus Runtime Codegen Fix

Status: `done`

Date: `2026-06-03`

Code commit: `EVAS 8930bb9`

Related paths:

- `EVAS/evas/simulator/backend.py`
- `EVAS/tests/test_indexed_backend.py`

## One-Line Summary

把 dynamic bus 节点名生成从嵌套 f-string 改成 `_format_dynamic_node()` helper，修复 state-index 表达式可能生成非法 Python 代码的风险。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| dynamic bus write codegen | 生成 `f'dout[{int(self.state['ch'])}]'` 形态的嵌套 f-string | 生成 `self._format_dynamic_node('dout', self.state['ch'])` | 语义不变 |
| dynamic bus read codegen | 同样依赖嵌套 f-string | 同样使用 helper | 语义不变 |
| tests | 只检查 dynamic metadata | 新增 state-index dynamic bus evaluate test | 锁住回归 |

## Principle

这个改动主要是 **Rust 化前置安全修复**，不是直接速度优化。

dynamic bus lowering 以后会把：

```text
dout[ch]
```

变成：

```text
base_node_id + offset(ch)
```

但在完全 indexed/Rust 化之前，Python runtime 仍要能正确格式化 `dout[1]` 这种节点名。之前代码把 index 表达式嵌进 f-string，如果 index 本身含有 `self.state['ch']`，就容易被引号打断。helper 方式先计算 index，再格式化字符串，避免 codegen 语法风险。

## Before / After Evidence

| Metric | Before | After | Interpretation |
|---|---:|---:|---|
| dynamic bus metadata | available | unchanged | 019 IR 没变 |
| generated dynamic code | nested f-string | helper call | 更稳 |
| state-index bus test | none | passed | 覆盖 `V(dout[ch])` |
| full pytest | n/a | 456 passed | 默认行为未回归 |

Validation commands:

```bash
python3 -m pytest tests/test_indexed_backend.py -q
python3 -m pytest tests -q
git diff --check
```

Important output:

```text
tests/test_indexed_backend.py: passed in targeted suite
full pytest: 456 passed
git diff --check: clean
```

## Functional Safety

- Default backend changed: `yes, but behavior-preserving codegen helper only`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`

## Learning Notes

Verilog-A 的 `V(dout[ch])` 不是编译期固定节点。`ch` 可能是 loop variable，也可能是 state dict 里的 integer。当前 Python runtime 仍用字符串节点名，所以必须先得到整数 index，再生成稳定节点字符串。

这一步没有把 dynamic bus 真正改成 `values[base + offset]`，只是先把旧字符串路径变稳。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| helper 格式和旧节点名不一致 | bus waveform/checker mismatch | 回退 `_format_dynamic_node()` codegen |
| 2D bus 格式错误 | 2D dynamic read/write tests 失败 | 回退 023 并补 2D fixture |

## Next Step

- `024 - Compiled Model Rust Replay Smoke`
