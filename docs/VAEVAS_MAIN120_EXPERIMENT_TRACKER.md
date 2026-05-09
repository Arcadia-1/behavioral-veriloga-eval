# vaEVAS Main120 Experiment Tracker

**Date**: 2026-05-08

| Run ID | Milestone | Purpose | System / Variant | Split | Metrics | Priority | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M120-R000 | M0 | Benchmark gate | gold | Main120 | semantic, integrity, EVAS, Spectre | MUST | DONE | Full EVAS/Spectre 120/120 |
| M120-R001 | M1 | Provider smoke | MiMo-V2.5-Pro A smoke | 5 Main120 tasks | API, extraction, token/time, truncation | MUST | DONE | generated 5/5, no API/no-code/truncation, reasoning_tokens=0; EVAS 0/5 shows prompt-only weakness not provider failure |
| M120-R002 | M2 | Base capability | A prompt-only, MiMo-V2.5-Pro | Main120 | Spectre PASS, compile, behavior, cost | MUST | DONE_EVAS_SPECTRE | strict-EVAS 18/120; Spectre 20/120; thinking disabled, max_tokens=4096, workers=8 |
| M120-R003 | M3 | Rule prompt delta | D rules-only, MiMo-V2.5-Pro | Main120 | delta over A | MUST | DONE_EVAS_SPECTRE | strict-EVAS-v2preflight 18/120; EVAS parityfix 21/120; Spectre 21/120; targeted splice reproduced full parityfix from 5 patched tasks; thinking disabled, max_tokens=4096, workers=8; input/output tokens=232370/54272 |
| M120-R004 | M3 | Compile feedback delta | C compile-loop | Main120 | compile closure, PASS, repair cost | MUST | TODO | Record loop count and feedback |
| M120-R005 | M3 | Skill prompt delta | S1 compile-skill-prompt | Main120 | PASS, compile, token cost | MUST | TODO | Skill in prompt only |
| M120-R006 | M3 | Accept/reject delta | S2 compile-skill-accept | Main120 | PASS, compile, runtime cost | MUST | TODO | Deterministic accept/reject |
| M120-R007 | M4 | Residual taxonomy | analyzer | Main120 D rows | failure family shares | MUST | DONE_D | Added normalized failure taxonomy without rewriting raw status; D EVAS/Spectre pair-level label-only mismatches: unsupported symbol 6, TB/source parse 4, conditional transition 1, interface source drive 1 |
| M120-R008 | M5 | Method triage | behavior/controller/RAG/compression decision | Main120 residuals | expected gain vs complexity | MUST | TODO | Pick at most two next mechanisms |
| M120-R009 | M6 | Heldout construction | gold | heldout48 | semantic, integrity, EVAS, Spectre | MUST | TODO | Do not tune on heldout |
| M120-R010 | M7 | Heldout transfer | selected methods | heldout48 | Spectre PASS, cost, residuals | MUST | TODO | Final generalization evidence |
