# Controller Literature Notes and Next Design - 2026-05-09

This note connects the current vaEVAS controller experiments to related LLM-agent patterns and proposes a next controller design.

## Current vaEVAS Evidence

The current compile path has these rows on Main120 with MiMo-V2.5-Pro:

| Row | Meaning | Spectre PASS | Spectre compile OK | Spectre compile fail |
| --- | --- | ---: | ---: | ---: |
| A | prompt-only | 20/120 | 48/120 | 72/120 |
| D | rules-only | 21/120 | 76/120 | 44/120 |
| C | compile-loop | 24/120 | 92/120 | 28/120 |
| S1 | compile-skill prompt | 28/120 | 108/120 | 12/120 |
| S2 | deterministic compile-skill accept/reject | 29/120 | 110/120 | 10/120 |
| T1 slice | LLM plan-execute fallback on S2 residual compile fails | 1/10 | 7/10 | 3/10 |

Targeted-splice estimate: applying T1 only to the 10 S2 Spectre compile-fail residuals moves Main120 from `29/120 PASS, 10/120 compile fail` to `30/120 PASS, 3/120 compile fail`. This is not a full-checkpoint replacement, but it is valid targeted evidence because only these residual candidates changed.

## What T1 Actually Adds

T1 is not simply another skill. It adds an online controller fallback:

1. Observe validator feedback from S2 residual failures.
2. Ask the LLM for a bounded compile-repair plan with root cause, current step, edit scope, expected validation delta, and forbidden edits.
3. Execute one repair step.
4. Run EVAS as the fast accept/reject gate.
5. Audit the targeted result with Spectre.

This addresses the closed-world limitation of S2: deterministic skills can only fix known patterns, while T1 can propose a repair for a novel residual. The cost is nonzero: 10 tasks, 28 API calls, 102426 input tokens, 9979 output tokens, 214.088 API seconds.

## Related Agent Patterns

### Plan-and-Solve / Plan-Execute

Plan-and-Solve prompting first creates a plan that decomposes the task, then solves the subtasks. For vaEVAS, this maps directly to generating a repair plan before editing Verilog-A/Spectre files.

Source: https://arxiv.org/abs/2305.04091

### ReAct

ReAct interleaves reasoning traces with actions and observations. For vaEVAS, the corresponding loop is `diagnose -> edit/tool -> EVAS observation -> replan`.

Source: https://arxiv.org/abs/2210.03629

### Reflexion / Self-Refine

Reflexion stores linguistic feedback after failed trials and reuses it in later attempts. For vaEVAS, failed repair traces can become memory entries indexed by failure family, e.g. `conditional_transition`, `pwl_empty`, `sourced_port_voltage_drive`, or `wrong_function_module`.

Source: https://arxiv.org/abs/2303.11366

### Toolformer / Tool Selection

Toolformer frames tool use as learning when to call tools and how to incorporate outputs. For vaEVAS, the controller should choose among deterministic skill tools, LLM repair tools, EVAS sub-checks, and Spectre audit.

Source: https://arxiv.org/abs/2302.04761

### ReWOO

ReWOO decouples reasoning from observations to reduce redundant prompting. For vaEVAS, this suggests a two-stage controller: plan once from compact diagnostics, then execute deterministic/validator tools without repeatedly sending full code and full history to the LLM.

Source: https://arxiv.org/abs/2305.18323

### Voyager

Voyager combines an automatic curriculum, an executable skill library, and iterative prompting with environment feedback. For vaEVAS, this supports a growing repair-skill library, but only if each skill is validated and indexed by public failure features instead of task ids.

Source: https://arxiv.org/abs/2305.16291

### SWE-agent / Agent-Computer Interface

SWE-agent argues that agent performance depends heavily on the environment interface. For vaEVAS, the interface should expose concise compile diagnostics, contract metadata, targeted EVAS commands, and safe patch scopes rather than raw long logs.

Source: https://arxiv.org/abs/2405.15793

### Context Engineering

The useful categories are write, select, compress, and isolate context. For vaEVAS:

- Write: save repair traces and validated failure memories outside the prompt.
- Select: retrieve only relevant skill cards and examples by failure family.
- Compress: summarize validator output and code diffs before LLM calls.
- Isolate: keep raw logs/results in state, only expose compact diagnostics to the LLM.

Source: https://www.langchain.com/blog/context-engineering-for-agents

## Proposed Controller v0.5

The next controller should be a typed state machine rather than a flat loop.

### State

Each task should carry:

| Field | Purpose |
| --- | --- |
| `task_id` | Stable id for storage only, not for routing decisions. |
| `public_contract` | Ports, task form, required signals, checker axes. |
| `failure_family` | Normalized validator failure families. |
| `compile_stage` | DUT/TB/interface/source/preflight. |
| `behavior_gap` | Compact metrics from checker. |
| `tool_history` | Tool calls, accepted/rejected status, token/time cost. |
| `memory_hits` | Retrieved prior repair traces or skill cards. |

### Tools

| Tool | When to call | Accept gate |
| --- | --- | --- |
| `local_compile_skill_batch` | Known strict compile patterns | EVAS compile rank improves |
| `llm_plan_execute_compile_repair` | Unknown compile residual or local skill stalled | EVAS rank improves, then Spectre targeted audit |
| `behavior_gap_diagnoser` | Compile OK but checker fails | EVAS behavior metric improves |
| `targeted_evas_subcheck` | Need cheap evidence for one axis | Axis-specific checker result |
| `spectre_checkpoint_audit` | PR/checkpoint/final table | Spectre result |

### Policy

1. Use deterministic local tools first when failure family has high-confidence fixers.
2. Use online LLM fallback only after local tools stall or the failure family is unknown.
3. Send compact diagnostics, public contract, minimal file snippets, and retrieved skill cards; do not send full task histories by default.
4. Store every accepted/rejected repair trace for later RAG/SFT.
5. Separate compile repair and behavior repair policies. Compile closure alone increasingly converts failures into behavior residuals; behavior repair now needs its own tools and metrics.

## Immediate Next Experiments

1. `T2-residual-compile`: run T1-style controller only on the three remaining T1 Spectre compile residuals. Goal: determine whether residual compile failure can be closed without adding hand-written skills.
2. `B1-behavior-gap-smoke`: select 8-12 compile-OK behavior failures across families and test a behavior-gap diagnoser with targeted EVAS subchecks.
3. `R0-repair-trace-index`: build a repair trace table from C/S1/S2/T1 with failure family, prompt snippet, edit summary, EVAS delta, Spectre delta, token/time.
4. `CTX1-compact-diagnostics`: compare T1 current prompt against compact-diagnostic prompt on the same 10 residuals to measure token reduction and compile-closure retention.

## Recommendation

The controller direction is justified, but the next optimization should not be “add more skills blindly.” The right path is:

1. Keep S2 as the cheap deterministic first pass.
2. Add T1-style online fallback only for residual compile errors or unknown families.
3. Build a trace/memory layer so successful repairs become reusable knowledge.
4. Start behavior-specific tools now, because compile closure is no longer the main bottleneck after S2/T1.
