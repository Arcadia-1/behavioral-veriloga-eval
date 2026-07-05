# Audit: Event Or Cross Timer

- Task id: `v3_456_event_or_cross_timer`
- Category: `veriloga_event_semantics`
- Gate 1 label: language-extension/L0 support row, not part of the original full-300 circuit-function claim.
- Independent value: exercises one flat analog event expression combining `cross()` and `timer()` with `or`.
- Duplicate boundary: distinct from `489-event-nested-or-expression` because this row is the minimal flat cross/timer event-or case, while 489 adds `above()` and a deeper combined event expression.
- Prompt status: updated to mandatory vaBench v3 section format and explicit L0/support boundary.
- Reference artifact: samples `vin` and increments `event_count` from one combined `cross(...) or timer(...)` event statement.
- Boundary: behavioral voltage-domain modeling only; no `I(...)` current contribution.
- Validation: EVAS reference run 7/7 PASS across S2 and 35/35 negative variants rejected; targeted Spectre visible/private reference runs 7/7 PASS and private negative variants 35/35 rejected; AHDL preflight 14/14 PASS with zero task-specific diagnostics.
