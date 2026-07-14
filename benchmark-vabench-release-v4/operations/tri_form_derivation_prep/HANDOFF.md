# Tri-Form Release Handoff

This lane derives Testbench and Bugfix task views without changing the frozen
DUT family assets.

## Materialized State

- Source provenance: `provenance/dut-base-v3-exact-five-hash-bound-v2`
- Source denominator SHA-256:
  `52278bac89017d62349a2577944cda8717bde78c3adef975280ba2bf988c643b`
- Families: 400
- DUT tasks: 400
- Testbench tasks: 400
- Bugfix tasks: 400
- G0-G5 prompt variants: 7,200, derived from `modes.json` and prompt component
  manifest rules rather than a committed JSONL prompt-record file
- Active mutations: exactly five per family, 2,000 total
- Bugfix seed: one member of the same five-mutation suite
- Materialization simulation reruns: 0
- Structure and bundle-isolation audit: PASS
- Release status: `materialized_gate3_audit_pending`

The tracked materialized package is `release/benchmarkv4/`. Its root is the
solver-facing public surface, and its `private_evaluator/` subdirectory
contains the gold references, mutation bundles, score policies, and derivation
records needed to run the benchmark scorer. The private evaluator assets are
tracked as part of the complete benchmark package; generated audit/runtime
evidence and optional prompt-record snapshots remain ignored.

## Remaining Release Work

1. merge the exact-five DUT and runner/checker prerequisite PR chain;
2. bind the final EVAS commit and executable identity;
3. run or carry forward hash-compatible evidence under the release policy;
4. execute the final private Spectre decision for frozen candidates;
5. rename/seal the package only after the strict release audit passes.

Runtime ingestion evidence proves that G0/G1 receive only the direct prompt and
that G2-G5 receive the public task bundle plus a writable submission directory.
It does not prove model success or final benchmark score.
