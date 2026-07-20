# DUT EVAS Guide

Write the declared DUT artifacts under `public/submission/`, then run:

`evas simulate public/task/visible_test.scs -o /tmp/vabench-visible/evas-output --spectre-strict`

The visible deck includes the current submission by relative path. Use the
simulation log and saved public traces to check interface, event, level,
timing, and metric behavior before finalizing the candidate.
