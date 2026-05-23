# vaBench Release Bridge Profile Diagnostics

Date: 2026-05-23

This report diagnoses the external bridge profiles needed for the
EVAS/Spectre release rerun. It is not benchmark certification evidence.

## Summary

| Metric | Value |
| --- | --- |
| status | `ready` |
| reason | bridge profile default is ready for release rerun |
| profiles | 3 |
| ready profiles | `default, ci, jin` |
| ssh-ok profiles | `none` |
| ssh-config-jump-ok profiles | `none` |
| ssh failure codes | `{"failed_unknown": 3}` |
| alt ssh failure codes | `{"failed_unknown": 2}` |
| hop ssh failure codes | `{"failed_unknown": 5}` |
| hop ssh ok routes | `none` |

## Profiles

| Profile | Remote | Jump | Local port | Hop SSH | SSH | Alt SSH | Preflight | Notes |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- |
| `default` | `jinzhihong@thu-wei` | `thu-sui` | 65082 | `explicit_jump:thu-sui:failed_unknown,ssh_config_proxyjump:thu-jin:failed_unknown` | `failed_unknown` | `ssh_config_proxyjump:failed_unknown` | `ok` | VB_JUMP_HOST=thu-sui differs from local ssh_config ProxyJump=thu-jin; try VB_USE_SSH_CONFIG_JUMP=1 if the explicit jump host times out |
| `ci` | `jinzhihong@thu-wei` | `thu-sui` | 65182 | `explicit_jump:thu-sui:failed_unknown,ssh_config_proxyjump:thu-jin:failed_unknown` | `failed_unknown` | `ssh_config_proxyjump:failed_unknown` | `ok` | VB_JUMP_HOST=thu-sui differs from local ssh_config ProxyJump=thu-jin; try VB_USE_SSH_CONFIG_JUMP=1 if the explicit jump host times out |
| `jin` | `jinzhihong@thu-wei` | `none` | 65084 | `ssh_config_proxyjump:thu-jin:failed_unknown` | `failed_unknown` | `none` | `ok` | no VB_JUMP_HOST is set; SSH smoke relies on local ssh_config ProxyJump=thu-jin |
