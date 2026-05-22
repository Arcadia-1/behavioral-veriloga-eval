# vaBench Release Bridge Profile Diagnostics

Date: 2026-05-21

This report diagnoses the external bridge profiles needed for the
EVAS/Spectre release rerun. It is not benchmark certification evidence.

## Summary

| Metric | Value |
| --- | --- |
| status | `ready` |
| reason | bridge profile ci is ready for release rerun |
| profiles | 3 |
| ready profiles | `ci` |
| ssh-ok profiles | `default, ci, jin` |
| ssh-config-jump-ok profiles | `default, ci` |
| ssh failure codes | `{"ok": 3}` |
| alt ssh failure codes | `{"ok": 2}` |
| hop ssh failure codes | `{"connect_timeout": 3, "ok": 2}` |
| hop ssh ok routes | `default:explicit_jump:thu-sui, ci:explicit_jump:thu-sui` |

## Profiles

| Profile | Remote | Jump | Local port | Hop SSH | SSH | Alt SSH | Preflight | Notes |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- |
| `default` | `jinzhihong@thu-wei` | `thu-sui` | 65082 | `explicit_jump:thu-sui:ok,ssh_config_proxyjump:thu-jin:connect_timeout` | `ok` | `ssh_config_proxyjump:ok` | `blocked` | VB_JUMP_HOST=thu-sui differs from local ssh_config ProxyJump=thu-jin; try VB_USE_SSH_CONFIG_JUMP=1 if the explicit jump host times out |
| `ci` | `jinzhihong@thu-wei` | `thu-sui` | 65182 | `explicit_jump:thu-sui:ok,ssh_config_proxyjump:thu-jin:connect_timeout` | `ok` | `ssh_config_proxyjump:ok` | `ok` | VB_JUMP_HOST=thu-sui differs from local ssh_config ProxyJump=thu-jin; try VB_USE_SSH_CONFIG_JUMP=1 if the explicit jump host times out |
| `jin` | `jinzhihong@thu-wei` | `none` | 65084 | `ssh_config_proxyjump:thu-jin:connect_timeout` | `ok` | `none` | `blocked` | no VB_JUMP_HOST is set; SSH smoke relies on local ssh_config ProxyJump=thu-jin |
