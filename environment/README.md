# Shared Harbor Environment

This directory is the canonical, task-agnostic agent environment for vaBench.
It intentionally contains only the Docker build inputs needed by the agent:

```text
environment/
├── Dockerfile
├── requirements.in
├── requirements.lock
└── runtime/
    └── entrypoint.sh
```

It must not contain benchmark tasks, hidden tests, checkers, gold solutions,
mutations, evaluator code, credentials, or generated simulation artifacts.

The runtime can be built and verified with:

```bash
benchmark-vabench-release-v4/public-agent-runtime/build.sh
benchmark-vabench-release-v4/public-agent-runtime/verify.sh
```

Harbor task materialization should copy this directory as
`<task>/environment/`, or point at an immutable image built from it. This is a
single shared source; task-specific Dockerfile copies are generated artifacts,
not independently maintained files.
