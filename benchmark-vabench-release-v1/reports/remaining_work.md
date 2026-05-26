# vaBench Release Remaining Work

Date: 2026-05-26

This report is the active queue for finishing the clean vaBench release.
It separates missing source design from missing simulator evidence and
from historical source-equivalence blockers. Scoring readiness is reported
from the frozen score denominator, not inferred from source presence alone.

## Summary

| Metric | Value |
| --- | ---: |
| planned entries | 64 |
| source-linked entries | 64 |
| entries with copied assets | 64 |
| static-certified release forms | 219 |
| dual-certified release forms | 217 |
| dual-pending release forms | 2 |
| dual-failed release forms | 0 |
| EVAS PASS / Spectre FAIL count | 0 |
| source-design pending entries | 0 |
| selected rerun-pending forms | 2 |
| source-equivalence blocked forms | 0 |
| fresh dual rerun queue forms | 2 |
| missing required-form entries | 0 |
| current seed missing-form entries | 0 |
| scored release entries | 51 |

## Source Design Pending

| Entry | Function | Missing forms |
| --- | --- | --- |
| none | none | none |

## Selected Rerun Pending

| Entry | Form | Source task |
| --- | --- | --- |
| `vbr1_l1_gain_estimator` | `tb` | `vbr1_l1_gain_estimator_tb` |
| `vbr1_l1_gain_estimator` | `e2e` | `vbr1_l1_gain_estimator_e2e` |

## Source-Equivalence Blocked

These rows are not a separate manual source-design queue. They are
historical-evidence import blockers that must be resolved by the
current fresh EVAS/Spectre rerun queue.

| Entry | Form | Source task | Blockers |
| --- | --- | --- | --- |
| none | none | none | none |

## Missing Required Forms

| Entry | Level | Package status | Missing forms |
| --- | --- | --- | --- |
| none | none | none | none |

## Current Seed Missing Forms

| Entry | Base | Missing forms |
| --- | --- | --- |
| none | none | none |

## Next Queue

- Run the current 2-form EVAS/Spectre fresh dual certification queue.
