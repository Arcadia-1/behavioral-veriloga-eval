# Bugfix EVAS Guide

The writable submission starts as an exact copy of the supplied buggy bundle.
Run the public deck directly after each meaningful edit:

`evas simulate public/task/visible_test.scs -o public/submission/evas-output --spectre-strict`

Use the simulation log and saved traces to test the repair while preserving
the declared file set, interfaces, and unaffected behavior.
