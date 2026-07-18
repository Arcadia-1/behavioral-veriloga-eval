# r45 Canonical Test Profile

r45 replaces the duplicated r44 `feedback` and `score` profiles with one
`canonical_test` profile. The profile describes test semantics only. Backend
selection, public visibility, and trusted evaluator placement are deployment
concerns and are not alternate test profiles.

The public visible test and final trusted replay must use byte-identical decks.
The generated profile records the deck SHA-256 and declares the reuse policy
`public_visible_and_final_trusted_replay_same_bytes`. A runtime exporter should
copy the same rendered deck to both surfaces and reject a hash mismatch.

## Migration

`render_r45_canonical_test.py` consumes one existing v4 `harness_spec.json`.
It first validates the v4 schema and requires feedback/score semantic parity.
It then records both legacy semantic hashes, emits one canonical semantic hash,
and renders one deck without backend-only options such as `evas_profile`.

Example:

```bash
python3 benchmark-vabench-release-v4/scripts/render_r45_canonical_test.py \
  --spec path/to/evaluator/harness_spec.json \
  --profile-output /tmp/canonical_test_profile.json \
  --deck-output /tmp/visible_test.scs
```

The command is intentionally per-family/per-task. Source shards may be migrated
in parallel, while the complete 1,200-task release is rebuilt only once by the
integration process. Existing r44 schemas, profiles, decks, manifests, and
release seals remain unchanged.
