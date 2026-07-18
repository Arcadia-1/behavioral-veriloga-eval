# Testbench EVAS Guide

The read-only task mount exposes a reference DUT and five mutation fixtures.
Their exact paths and direct command template are in `evas_runtime.json`.
First run the public reference deck:

`evas simulate public/task/visible_test.scs -o public/submission/evas-output/reference --spectre-strict`

To test the candidate, copy `testbench.scs` into a writable per-case run
directory, bind that directory's `dut` path to one listed read-only fixture,
and invoke `evas simulate` on the copied candidate. Repeat for the reference
and all five mutations. The final replay uses these same six fixtures.
