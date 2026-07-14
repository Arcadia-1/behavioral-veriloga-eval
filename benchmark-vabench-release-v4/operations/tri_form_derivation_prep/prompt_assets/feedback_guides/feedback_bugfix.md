# Bugfix Feedback Guide

The feedback CLI is an inspectable measurement surface, not a prescribed
repair recipe. Query its capabilities and request whichever available channels
best test the current hypothesis: artifact validation, AHDL-like diagnostics,
simulation logs, public traces, metrics, or property diagnostics.

For repairs, the agent may run the original bundle, an intermediate edit, or
the final candidate. Use feedback to test a hypothesis against the complete
public contract while preserving unaffected behavior and the declared bundle
structure.

Use expected/observed values, event times, mismatch counts, metric gaps, and
traces when they are useful. Distinguish artifact, compile, runtime,
missing-trace, and behavioral failures.

Feedback is not the private Spectre score. Preserve the public contract and do
not infer evaluator paths, checker source, hidden constants, or mutation code.
