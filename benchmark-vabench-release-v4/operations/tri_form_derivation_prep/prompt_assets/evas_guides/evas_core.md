# Direct EVAS Guide

Use the installed `evas` executable directly. The public task mount contains
the complete visible test and `evas_runtime.json`; the writable submission
mount contains the candidate and all generated simulator output.

Run `evas simulate` with `--spectre-strict`. Inspect its log and generated
`tran.csv` waveforms when testing a hypothesis. EVAS does not return a private
score, checker decision, gold comparison, or hidden diagnostic. The final
trusted replay uses the same test bytes and fixtures exposed here.

Do not edit the read-only task mount. Do not look for evaluator source, gold,
hidden parameters, or a feedback broker; none is part of the public runtime.
