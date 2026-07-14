# Testbench Feedback Guide

The feedback CLI is an inspectable measurement surface, not a prescribed
repair recipe. Query its capabilities and request whichever available channels
best test the current hypothesis: artifact validation, AHDL-like diagnostics,
simulation logs, public traces, metrics, or property diagnostics.

One feedback request runs the unchanged candidate testbench against the
supplied correct DUT and five anonymous negative DUT cases. Interpret correct
DUT failure, survived negative behavior, behavioral kills, invalid runs, and
missing traces as different outcomes.

Use expected/observed values, event times, mismatch counts, metric gaps, and
traces when they are useful. Negative source, fault labels, checker internals,
and private score decisions are not available.

Feedback is not the private Spectre score. Preserve the public contract and do
not infer evaluator paths, checker source, hidden constants, or mutation code.
