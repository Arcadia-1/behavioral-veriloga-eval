# NNN - <Change Title>

Status: `planned | active | done | diagnostic | rejected`

Date: `<YYYY-MM-DD>`

Code commit: `<EVAS commit hash or pending>`

Related reports:

- `<path>`

## One-Line Summary

用一句话说明这次改动解决什么瓶颈。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| `<parser/backend/kernel/checker>` | `<old path>` | `<new path>` | `<unchanged/changed>` |

## Principle

说明为什么这个改动应该更快。优先用下面三类语言：

- **降低每步成本**：例如把 `dict[str, float]` 改成 node id + array。
- **减少仿真步数**：例如 event queue 直接跳到下一个 timer/cross/breakpoint。
- **减少输出/检查开销**：例如只记录 checker 必需信号。

如果没有明确属于哪一类，这个改动不应该被当作速度优化主线。

## Before / After Evidence

| Metric | Before | After | Interpretation |
|---|---:|---:|---|
| EVAS subprocess wall | `<s>` | `<s>` | `<faster/slower/unchanged>` |
| accepted steps | `<count>` | `<count>` | `<step-count impact>` |
| per-step cost | `<us/step>` | `<us/step>` | `<kernel cost impact>` |
| checker/result parity | `<status>` | `<status>` | `<accuracy/function impact>` |

## Functional Safety

- Default backend changed: `yes/no`
- CSV schema changed: `yes/no`
- `strobe.txt` behavior changed: `yes/no`
- Checker behavior changed: `yes/no`
- Fallback path exists: `yes/no`

## Validation

Commands run:

```bash
<command>
```

Results:

```text
<important output>
```

## Learning Notes

用初学者能理解的方式解释这次涉及的概念。例如：

- 什么是 node id？
- 为什么 Rust `Vec<f64>` 比 Python dict 快？
- 什么是 event queue？
- 为什么仿真器不能只看 wall time，还要看 parity？

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| `<risk>` | `<test/report showing it>` | `<file/commit/path to revert>` |

## Next Step

下一篇审计文档编号和预期主题：

- `NNN+1 - <next topic>`
