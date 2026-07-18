# benchmarkv4 runners

This directory contains public runtime tooling for
`benchmark-vabench-release-v4/release/benchmarkv4`.

Implemented:

- `run_benchmarkv4_campaign.py` is the unified experiment entry point for
  `release/benchmarkv4`: it builds a random or preselected campaign, then runs
  `G0`/`G1` through direct one-shot artifact extraction and `G2`-`G5` through
  the real agentic filesystem plus restricted visible-EVAS loop. Both paths enter the
  same strict declared-artifact gate before they become score-eligible.

Boundary:

- The campaign runner is a generation/materialization runner, not the final
  Spectre scorer.
- Faithful single-turn API runs are `G0` and `G1`. `G2`-`G5` can read and write
  their isolated workspace and invoke only the public `run_evas` contract;
  they cannot query a checker, gold solution, mutation catalog, or score.
- Deprecated API-only and initial-judge entry points were removed from this
  package to keep one comparable G0-G5 path.

Unified G0-G5 campaign example:

```bash
python3 benchmark-vabench-release-v4/runners/run_benchmarkv4_campaign.py \
  --sample-families 10 \
  --seed 20260715 \
  --model deepseek-v4-flash \
  --base-url https://api.deepseek.com/v1 \
  --api-key-file /path/to/key.txt \
  --max-working-tokens 65536 \
  --workers 12 \
  --output-root /tmp/benchmarkv4-deepseek-campaign
```

Dry-run preflight without API credentials:

```bash
python3 benchmark-vabench-release-v4/runners/run_benchmarkv4_campaign.py \
  --task-id v4-001 \
  --mode G0 \
  --model deepseek-v4-flash \
  --dry-run \
  --output-root /tmp/benchmarkv4-campaign-dry-run
```

Final trusted replay for a completed campaign:

```bash
python3 benchmark-vabench-release-v4/operations/calibration_pilot/score_campaign.py \
  --campaign-output /tmp/benchmarkv4-deepseek-campaign/run \
  --judge-kind final_trusted_replay \
  --judge-command \
    "python3 /path/to/trusted_replay_adapter.py"
```
