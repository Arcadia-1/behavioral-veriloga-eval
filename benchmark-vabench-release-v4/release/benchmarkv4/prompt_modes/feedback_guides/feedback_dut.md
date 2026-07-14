# DUT Feedback Guide

The feedback CLI is an inspectable measurement surface, not a prescribed
repair recipe. Query its capabilities and request whichever available channels
best test the current hypothesis: artifact validation, AHDL-like diagnostics,
simulation logs, public traces, metrics, or property diagnostics.

For DUT candidates, use public-property diagnostics and traces to compare the
implemented response with the declared interface, event semantics, levels,
timing, and metrics. Distinguish artifact, compile, runtime, missing-trace, and
behavioral failures.

Use expected/observed values, event times, mismatch counts, metric gaps, and
traces when they are useful. A passing feedback case is useful evidence but
does not replace a final contract audit.

Feedback is not the private Spectre score. Preserve the public contract and do
not infer evaluator paths, checker source, hidden constants, or mutation code.
