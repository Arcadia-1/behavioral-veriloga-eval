# Raw Speed Result Policy

Raw speed run outputs are intentionally not moved here.

Local raw output directories currently include:

- `../results/evas-speed-p0-p3-smoke-pfdsmall-20260521`
- `../results/evas-speed-p0-p3-pilot-20260521`
- `../results/evas-speed-p0-p3-smoke-pfd-20260521`
- `../results/evas-speed-p0-p3-smoke-20260521`
- `../results/evas-speed-p0-p3-smoke-20260521b`
- `../results/vabench-release-v1-dual-rerun-speed-remaining-smoke-20260521-bridge-retry`
- `../results/vabench-release-v1-dual-rerun-speed-remaining-fix9-20260521`
- `../results/vabench-release-v1-dual-rerun-speed-remaining-20260521`
- `../results/vabench-release-v1-dual-rerun-speed-remaining-20260519`

These trees are generated data. They can be kept locally for debugging, but the versioned speed evidence should be the compact reports under `../reports/`.

Server-side raw roots should be recorded in the report JSON `output_root` fields or in a dedicated run log, not copied wholesale into Git.
