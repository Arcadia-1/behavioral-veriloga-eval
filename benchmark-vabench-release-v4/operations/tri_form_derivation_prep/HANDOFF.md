# Tri-Form Release Handoff

This lane derives Testbench and Bugfix task views without changing the frozen
DUT family assets.

## Materialized State

- Source release: `release/dut-base-v3-exact-five-hash-bound-v2`
- Source denominator SHA-256:
  `52278bac89017d62349a2577944cda8717bde78c3adef975280ba2bf988c643b`
- Families: 400
- DUT tasks: 400
- Testbench tasks: 400
- Bugfix tasks: 400
- G0-G5 prompt records: 7,200
- Active mutations: exactly five per family, 2,000 total
- Bugfix seed: one member of the same five-mutation suite
- Materialization simulation reruns: 0
- Hash-incompatible source evidence: retained as an evidence-rebinding queue;
  materialization does not classify it as a mandatory simulator rerun
- Structure and bundle-isolation audit: PASS
- Materializer status: `package_materialized_behavior_evidence_pending`
- Static seal status after audit: `package_structure_sealed`

The materialized package is
`release/tri-form-v4-1200-final/`. This is the fixed static benchmark package
for runner and prompt use. Final EVAS/Spectre behavior claims still require a
separate frozen-toolchain evidence gate.
The task definitions themselves are generated for all 1,200 IDs.

The current pre-EVAS evidence boundary, counts, and hashes are summarized in
`PRE_EVAS_CLOSEOUT.md` and `PRE_EVAS_CLOSEOUT.json`. Those files are a
checkpoint, not a final behavior seal.

## Remaining Release Work

1. merge the exact-five DUT and runner/checker prerequisite PR chain;
2. bind the final EVAS commit and executable identity;
3. run or carry forward hash-compatible evidence under the release policy;
4. execute the final private Spectre decision for frozen candidates;
5. rename/seal the package only after the strict release audit passes.

Runtime ingestion evidence proves that G0/G1 receive only the direct prompt and
that G2-G5 receive the public task bundle plus a writable submission directory.
It does not prove model success or final benchmark score.
