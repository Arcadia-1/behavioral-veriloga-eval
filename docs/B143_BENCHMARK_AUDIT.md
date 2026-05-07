# b143 Benchmark Audit

**Date**: 2026-05-07

This audit checks whether `benchmark-balanced` / `b143` should be modified after
cleaning the project narrative.

## Current Structure

`b143` contains 143 tasks.

| Task form | Count |
| --- | ---: |
| `bugfix` | 25 |
| `dut-only/spec-to-va` | 33 |
| `end-to-end` | 62 |
| `tb-generation` | 23 |

It covers 22 `core_function` families.  Every core-function family has at least
one task in each of the four task forms:

```text
missing_core_form = []
```

Therefore the benchmark is **task-form covered**, not count-equal across task
forms.

## Exact Four-Form Packs

The current exact one-per-form packs are:

| Core function | Forms |
| --- | --- |
| `threshold_detector` | bugfix, spec-to-va, end-to-end, tb-generation |
| `window_detector` | bugfix, spec-to-va, end-to-end, tb-generation |
| `analog_limiter` | bugfix, spec-to-va, end-to-end, tb-generation |
| `pulse_stretcher` | bugfix, spec-to-va, end-to-end, tb-generation |

Other core functions have all four task forms represented, but not exactly one
instance per form.  For example, some inherited families have many end-to-end
variants.

## Does The Benchmark Need Modification Now?

No immediate task-content modification is required for the current paper
mainline.  The benchmark is already usable for:

1. full 143-task main results,
2. task-form breakdowns,
3. core-function breakdowns,
4. residual failure taxonomy.

The required correction is primarily narrative/metadata: do not describe the
benchmark as four count-equal buckets, and do not define it by source provenance.
Describe it as 143 tasks with task-form coverage across 22 circuit-function
families.

## Potential Issues To Review Before Future Expansion

| Issue | Risk | Recommended action |
| --- | --- | --- |
| `benchmark-balanced` name | Readers may infer equal counts across task forms. | Keep path for compatibility, but use `b143` in paper text and explain task-form coverage. |
| Mixed `task_form` strings | Both `spec-to-va` and `dut-only/spec-to-va` appear in metadata. | Normalize reporting to `spec-to-va`; keep raw metadata only if loaders require it. |
| Large inherited end-to-end weight | `end-to-end=62/143`, so aggregate pass rate may be influenced by end-to-end-heavy families. | Always report task-form breakdown alongside full `PASS/143`. |
| Core-function granularity | Some labels are broad (`digital-logic`, `stimulus`), others narrow (`analog_limiter`). | Use current labels for this paper; refine ontology only in a future benchmark version. |
| Observable duplicate risk | Same broad core function may contain multiple related tasks. | Audit duplicates by observable behavior before adding new tasks; do not remove current tasks without a separate benchmark-version decision. |

## Future Addition Rule

Future additions should be made as function-family packs.  The separate plan for
an exact pack benchmark is `docs/BPACK_BENCHMARK_PLAN.md`.

```text
one circuit-function family
-> relevant task forms: bugfix / spec-to-va / end-to-end / tb-generation
-> no duplicate observable behavior
-> gold validated by strict-evas and targeted spectre-audit before promotion
```

A future `b143-v2` or larger benchmark should explicitly say whether it is:

1. task-form covered, or
2. count-equal across task forms, or
3. stratified by core-function family.

The current `b143` should not be retroactively forced into count-equal balance;
that would change the benchmark and require rerunning main results.
