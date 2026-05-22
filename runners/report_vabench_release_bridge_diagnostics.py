#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
from collections import Counter
from datetime import date
from pathlib import Path

from bridge_preflight import bridge_preflight, load_env_pairs, resolve_cadence_cshrc, resolve_local_port


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
REPORTS_ROOT = PACKAGE_ROOT / "reports"
DEFAULT_BRIDGE_REPO = ROOT.parents[1] / "iccad" / "virtuoso-bridge-lite"
REPORT_JSON = REPORTS_ROOT / "bridge_profile_diagnostics.json"
REPORT_MD = REPORTS_ROOT / "bridge_profile_diagnostics.md"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def env_key(key: str, profile: str | None) -> str:
    return f"{key}_{profile}" if profile else key


def discover_profiles(env_pairs: dict[str, str]) -> list[str | None]:
    profiles: set[str | None] = {None}
    prefix = "VB_REMOTE_HOST_"
    for key in env_pairs:
        if key.startswith(prefix):
            profiles.add(key[len(prefix) :])
    return sorted(profiles, key=lambda item: item or "")


def value_for(env_pairs: dict[str, str], key: str, profile: str | None, default: str = "") -> str:
    profiled = env_key(key, profile)
    if profiled in os.environ:
        return os.environ[profiled]
    if key in os.environ:
        return os.environ[key]
    if profiled in env_pairs:
        return env_pairs[profiled]
    return env_pairs.get(key, default)


def ssh_config(host: str, timeout_s: int) -> dict[str, str]:
    if not host:
        return {}
    try:
        proc = subprocess.run(
            ["ssh", "-G", host],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout_s,
        )
    except (OSError, subprocess.TimeoutExpired):
        return {}
    fields = {"hostname", "user", "port", "proxyjump", "proxycommand", "identityfile"}
    config: dict[str, str] = {}
    for raw in proc.stdout.splitlines():
        if " " not in raw:
            continue
        key, value = raw.split(None, 1)
        if key in fields and key not in config:
            config[key] = value.strip()
    return config


def parse_proxyjump_target(proxyjump: str, fallback_user: str) -> tuple[str, str]:
    first_hop = proxyjump.split(",", 1)[0].strip()
    if not first_hop or first_hop.lower() == "none":
        return "", ""
    if "@" in first_hop:
        user, host = first_hop.split("@", 1)
    else:
        user, host = fallback_user, first_hop
    host = host.strip()
    if host.startswith("[") and "]" in host:
        host = host[1 : host.index("]")]
    elif ":" in host:
        host = host.split(":", 1)[0]
    return host, user.strip()


def classify_ssh_failure(status: str, stdout: str, stderr: str) -> dict[str, object]:
    text = f"{stdout}\n{stderr}".lower()
    if status == "ok":
        return {
            "failure_code": "ok",
            "failure_summary": "ssh echo smoke succeeded",
            "remediation": [],
        }
    if status == "skipped":
        return {
            "failure_code": "skipped",
            "failure_summary": "ssh smoke skipped",
            "remediation": [],
        }
    if "timed out during banner exchange" in text:
        return {
            "failure_code": "banner_timeout",
            "failure_summary": "SSH reached a TCP connection path but timed out during banner exchange",
            "remediation": [
                "Check VPN/bastion reachability and whether the jump host accepts SSH sessions.",
                "Retry with a longer VB_SSH_CONNECT_TIMEOUT only after confirming the route is valid.",
            ],
        }
    if "connection timed out" in text or "operation timed out" in text:
        return {
            "failure_code": "connect_timeout",
            "failure_summary": "SSH connection timed out before authentication",
            "remediation": [
                "Check network/VPN reachability to the target or jump host.",
                "Compare explicit VB_JUMP_HOST routing with the local ssh_config ProxyJump route.",
            ],
        }
    if "permission denied" in text:
        return {
            "failure_code": "auth_failed",
            "failure_summary": "SSH authentication failed",
            "remediation": [
                "Check SSH keys, remote username, and BatchMode-compatible authentication.",
            ],
        }
    if "could not resolve hostname" in text or "name or service not known" in text:
        return {
            "failure_code": "dns_failed",
            "failure_summary": "SSH host name could not be resolved",
            "remediation": [
                "Check VB_REMOTE_HOST, VB_JUMP_HOST, and local ssh_config Host aliases.",
            ],
        }
    if "connection refused" in text:
        return {
            "failure_code": "connection_refused",
            "failure_summary": "SSH port refused the connection",
            "remediation": [
                "Check that sshd is running on the target or jump host and the configured port is correct.",
            ],
        }
    if "no route to host" in text:
        return {
            "failure_code": "no_route",
            "failure_summary": "Network reported no route to host",
            "remediation": [
                "Check VPN/routing state before retrying the release rerun.",
            ],
        }
    if "host key verification failed" in text:
        return {
            "failure_code": "host_key_failed",
            "failure_summary": "SSH host key verification failed",
            "remediation": [
                "Refresh the known_hosts entry or verify the host key out of band.",
            ],
        }
    if status == "timeout":
        return {
            "failure_code": "command_timeout",
            "failure_summary": "SSH smoke command exceeded the diagnostics timeout",
            "remediation": [
                "Increase --ssh-timeout-s only after checking route health.",
            ],
        }
    return {
        "failure_code": "failed_unknown",
        "failure_summary": "SSH smoke failed with an unclassified error",
        "remediation": [
            "Inspect stdout_tail/stderr_tail in bridge_profile_diagnostics.json.",
        ],
    }


def ssh_smoke(
    *,
    remote_host: str,
    remote_user: str,
    jump_host: str,
    jump_user: str,
    timeout_s: int,
) -> dict[str, object]:
    if not remote_host or not remote_user:
        return {
            "status": "skipped",
            "reason": "missing remote host or user",
            "command": [],
            "returncode": None,
            "stdout_tail": "",
            "stderr_tail": "",
            **classify_ssh_failure("skipped", "", ""),
        }
    target = f"{remote_user}@{remote_host}"
    cmd = [
        "ssh",
        "-o",
        "BatchMode=yes",
        "-o",
        f"ConnectTimeout={timeout_s}",
        "-o",
        "ServerAliveInterval=2",
        "-o",
        "ServerAliveCountMax=1",
        "-o",
        "StrictHostKeyChecking=no",
        "-o",
        "LogLevel=ERROR",
    ]
    if jump_host:
        cmd.extend(["-J", f"{jump_user or remote_user}@{jump_host}"])
    cmd.extend([target, "echo ok"])
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
            timeout=max(timeout_s + 5, 8),
        )
        stdout = proc.stdout or ""
        stderr = proc.stderr or ""
        ok = proc.returncode == 0 and "ok" in stdout.split()
        status = "ok" if ok else "failed"
        return {
            "status": status,
            "returncode": proc.returncode,
            "command": redacted_ssh_command(cmd),
            "stdout_tail": stdout[-1000:],
            "stderr_tail": stderr[-1000:],
            **classify_ssh_failure(status, stdout, stderr),
        }
    except subprocess.TimeoutExpired as exc:
        stdout = (exc.stdout or "")[-1000:] if isinstance(exc.stdout, str) else ""
        stderr = (exc.stderr or "")[-1000:] if isinstance(exc.stderr, str) else ""
        return {
            "status": "timeout",
            "returncode": None,
            "command": redacted_ssh_command(cmd),
            "stdout_tail": stdout,
            "stderr_tail": stderr,
            **classify_ssh_failure("timeout", stdout, stderr),
        }


def redacted_ssh_command(cmd: list[str]) -> list[str]:
    redacted: list[str] = []
    for item in cmd:
        if "@" in item and not item.startswith("-"):
            user, host = item.split("@", 1)
            redacted.append(f"{user[:1]}***@{host}")
        else:
            redacted.append(item)
    return redacted


def cached_ssh_smoke(
    cache: dict[tuple[str, str, str, str, int], dict[str, object]],
    *,
    remote_host: str,
    remote_user: str,
    jump_host: str,
    jump_user: str,
    timeout_s: int,
) -> dict[str, object]:
    key = (remote_host, remote_user, jump_host, jump_user, timeout_s)
    if key not in cache:
        cache[key] = ssh_smoke(
            remote_host=remote_host,
            remote_user=remote_user,
            jump_host=jump_host,
            jump_user=jump_user,
            timeout_s=timeout_s,
        )
    return dict(cache[key])


def hop_ssh_smokes(
    *,
    jump_host: str,
    jump_user: str,
    remote_user: str,
    config_proxyjump: str,
    timeout_s: int,
    skip_ssh: bool,
    cache: dict[tuple[str, str, str, str, int], dict[str, object]],
) -> list[dict[str, object]]:
    if skip_ssh:
        return []
    hops: list[dict[str, str]] = []
    if jump_host:
        hops.append({"route": "explicit_jump", "host": jump_host, "user": jump_user or remote_user})
    proxy_host, proxy_user = parse_proxyjump_target(config_proxyjump, remote_user)
    if proxy_host:
        hops.append({"route": "ssh_config_proxyjump", "host": proxy_host, "user": proxy_user or remote_user})
    records: list[dict[str, object]] = []
    seen: set[tuple[str, str, str]] = set()
    for hop in hops:
        key = (hop["route"], hop["host"], hop["user"])
        if key in seen:
            continue
        seen.add(key)
        records.append(
            {
                "route": hop["route"],
                "target_host": hop["host"],
                "target_user": hop["user"],
                "ssh_smoke": cached_ssh_smoke(
                    cache,
                    remote_host=hop["host"],
                    remote_user=hop["user"],
                    jump_host="",
                    jump_user="",
                    timeout_s=timeout_s,
                ),
            }
        )
    return records


def profile_record(
    bridge_repo: Path,
    env_pairs: dict[str, str],
    profile: str | None,
    *,
    ssh_timeout_s: int,
    skip_ssh: bool,
    smoke_cache: dict[tuple[str, str, str, str, int], dict[str, object]],
) -> dict[str, object]:
    remote_host = value_for(env_pairs, "VB_REMOTE_HOST", profile)
    remote_user = value_for(env_pairs, "VB_REMOTE_USER", profile)
    jump_host = value_for(env_pairs, "VB_JUMP_HOST", profile)
    jump_user = value_for(env_pairs, "VB_JUMP_USER", profile)
    remote_port = value_for(env_pairs, "VB_REMOTE_PORT", profile, "65081")
    local_port = resolve_local_port(bridge_repo, profile)
    cadence_cshrc = resolve_cadence_cshrc(bridge_repo, profile=profile)
    use_ssh_config_jump = value_for(env_pairs, "VB_USE_SSH_CONFIG_JUMP", profile, "0") == "1"
    config = ssh_config(remote_host, ssh_timeout_s)
    diagnostic_notes: list[str] = []
    config_proxyjump = str(config.get("proxyjump", "")).strip()
    smoke_jump_host = "" if use_ssh_config_jump else jump_host
    smoke_jump_user = "" if use_ssh_config_jump else jump_user
    if use_ssh_config_jump:
        diagnostic_notes.append(
            f"VB_USE_SSH_CONFIG_JUMP=1; SSH smoke lets local ssh_config route ProxyJump={config_proxyjump or 'none'}"
        )
    elif jump_host and config_proxyjump and config_proxyjump != jump_host:
        diagnostic_notes.append(
            f"VB_JUMP_HOST={jump_host} differs from local ssh_config ProxyJump={config_proxyjump}; "
            "try VB_USE_SSH_CONFIG_JUMP=1 if the explicit jump host times out"
        )
    elif not jump_host and config_proxyjump:
        diagnostic_notes.append(
            f"no VB_JUMP_HOST is set; SSH smoke relies on local ssh_config ProxyJump={config_proxyjump}"
        )
    preflight = bridge_preflight(
        bridge_repo,
        cadence_cshrc=cadence_cshrc,
        require_daemon=False,
        timeout_s=max(ssh_timeout_s, 5),
        profile=profile,
    )
    ssh = (
        {"status": "skipped", "reason": "skip_ssh requested"}
        if skip_ssh
        else cached_ssh_smoke(
            smoke_cache,
            remote_host=remote_host,
            remote_user=remote_user,
            jump_host=smoke_jump_host,
            jump_user=smoke_jump_user,
            timeout_s=ssh_timeout_s,
        )
    )
    alternate_ssh_smokes: list[dict[str, object]] = []
    if not skip_ssh and not use_ssh_config_jump and jump_host and config_proxyjump and config_proxyjump != jump_host:
        alternate_ssh_smokes.append(
            {
                "route": "ssh_config_proxyjump",
                "env": "VB_USE_SSH_CONFIG_JUMP=1",
                "ssh_smoke": cached_ssh_smoke(
                    smoke_cache,
                    remote_host=remote_host,
                    remote_user=remote_user,
                    jump_host="",
                    jump_user="",
                    timeout_s=ssh_timeout_s,
                ),
            }
        )
    hop_smokes = hop_ssh_smokes(
        jump_host=jump_host,
        jump_user=jump_user,
        remote_user=remote_user,
        config_proxyjump=config_proxyjump,
        timeout_s=ssh_timeout_s,
        skip_ssh=skip_ssh,
        cache=smoke_cache,
    )
    return {
        "profile": profile or "default",
        "remote_host": remote_host,
        "remote_user": remote_user,
        "jump_host": jump_host,
        "jump_user": jump_user,
        "use_ssh_config_jump": use_ssh_config_jump,
        "remote_port": remote_port,
        "local_port": local_port,
        "cadence_cshrc": cadence_cshrc,
        "ssh_config": config,
        "diagnostic_notes": diagnostic_notes,
        "hop_ssh_smokes": hop_smokes,
        "ssh_smoke": ssh,
        "alternate_ssh_smokes": alternate_ssh_smokes,
        "preflight": preflight,
        "ready_for_release_rerun": preflight.get("status") == "ok",
    }


def build_report(bridge_repo: Path, *, ssh_timeout_s: int, skip_ssh: bool) -> dict[str, object]:
    bridge_repo = bridge_repo.resolve()
    env_pairs = load_env_pairs(bridge_repo / ".env")
    profiles = discover_profiles(env_pairs)
    smoke_cache: dict[tuple[str, str, str, str, int], dict[str, object]] = {}
    records = [
        profile_record(
            bridge_repo,
            env_pairs,
            profile,
            ssh_timeout_s=ssh_timeout_s,
            skip_ssh=skip_ssh,
            smoke_cache=smoke_cache,
        )
        for profile in profiles
    ]
    ready_profiles = [record["profile"] for record in records if record["ready_for_release_rerun"]]
    ssh_ok_profiles = [
        record["profile"]
        for record in records
        if isinstance(record.get("ssh_smoke"), dict) and record["ssh_smoke"].get("status") == "ok"
    ]
    ssh_config_jump_ok_profiles = [
        record["profile"]
        for record in records
        for alternate in record.get("alternate_ssh_smokes", [])
        if isinstance(alternate, dict)
        and isinstance(alternate.get("ssh_smoke"), dict)
        and alternate["ssh_smoke"].get("status") == "ok"
    ]
    failure_codes = Counter(
        str(record.get("ssh_smoke", {}).get("failure_code", "missing"))
        for record in records
        if isinstance(record.get("ssh_smoke"), dict)
    )
    alternate_failure_codes = Counter(
        str(alternate.get("ssh_smoke", {}).get("failure_code", "missing"))
        for record in records
        for alternate in record.get("alternate_ssh_smokes", [])
        if isinstance(alternate, dict) and isinstance(alternate.get("ssh_smoke"), dict)
    )
    hop_failure_codes = Counter(
        str(hop.get("ssh_smoke", {}).get("failure_code", "missing"))
        for record in records
        for hop in record.get("hop_ssh_smokes", [])
        if isinstance(hop, dict) and isinstance(hop.get("ssh_smoke"), dict)
    )
    hop_ok_routes = [
        f"{record['profile']}:{hop.get('route')}:{hop.get('target_host')}"
        for record in records
        for hop in record.get("hop_ssh_smokes", [])
        if isinstance(hop, dict)
        and isinstance(hop.get("ssh_smoke"), dict)
        and hop["ssh_smoke"].get("status") == "ok"
    ]
    if ready_profiles:
        status = "ready"
        reason = f"bridge profile {ready_profiles[0]} is ready for release rerun"
    elif ssh_ok_profiles:
        status = "blocked"
        reason = "SSH reaches at least one profile, but bridge tunnel/daemon/Spectre preflight is not ready"
    elif ssh_config_jump_ok_profiles:
        status = "blocked"
        reason = "SSH reaches at least one ssh_config jump route; rerun with VB_USE_SSH_CONFIG_JUMP=1 and then check bridge preflight"
    elif skip_ssh:
        status = "blocked"
        reason = "bridge preflight is blocked; SSH smoke was skipped"
    elif failure_codes and failure_codes.most_common(1)[0][0] == "banner_timeout":
        status = "blocked"
        reason = "all bridge SSH profile smokes failed during banner exchange"
    else:
        status = "blocked"
        reason = "all bridge SSH profile smokes failed or timed out"
    return {
        "date": date.today().isoformat(),
        "release": "vabench-release-v1",
        "status": status,
        "reason": reason,
        "bridge_repo": str(bridge_repo),
        "profile_count": len(records),
        "ready_profiles": ready_profiles,
        "ssh_ok_profiles": ssh_ok_profiles,
        "ssh_config_jump_ok_profiles": ssh_config_jump_ok_profiles,
        "ssh_failure_code_counts": dict(sorted(failure_codes.items())),
        "alternate_ssh_failure_code_counts": dict(sorted(alternate_failure_codes.items())),
        "hop_ssh_failure_code_counts": dict(sorted(hop_failure_codes.items())),
        "hop_ssh_ok_routes": hop_ok_routes,
        "ssh_timeout_s": ssh_timeout_s,
        "skip_ssh": skip_ssh,
        "profiles": records,
        "notes": [
            "This is bridge readiness evidence only; it is not EVAS/Spectre certification evidence.",
            "Use BRIDGE_PROFILE=<profile> with scripts/run_with_bridge.sh to select a profile for release rerun.",
        ],
    }


def write_markdown(report: dict[str, object]) -> None:
    lines = [
        "# vaBench Release Bridge Profile Diagnostics",
        "",
        f"Date: {report['date']}",
        "",
        "This report diagnoses the external bridge profiles needed for the",
        "EVAS/Spectre release rerun. It is not benchmark certification evidence.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | --- |",
        f"| status | `{report['status']}` |",
        f"| reason | {report['reason']} |",
        f"| profiles | {report['profile_count']} |",
        f"| ready profiles | `{', '.join(report['ready_profiles']) or 'none'}` |",
        f"| ssh-ok profiles | `{', '.join(report['ssh_ok_profiles']) or 'none'}` |",
        f"| ssh-config-jump-ok profiles | `{', '.join(report['ssh_config_jump_ok_profiles']) or 'none'}` |",
        f"| ssh failure codes | `{json.dumps(report['ssh_failure_code_counts'], sort_keys=True)}` |",
        f"| alt ssh failure codes | `{json.dumps(report['alternate_ssh_failure_code_counts'], sort_keys=True)}` |",
        f"| hop ssh failure codes | `{json.dumps(report['hop_ssh_failure_code_counts'], sort_keys=True)}` |",
        f"| hop ssh ok routes | `{', '.join(report['hop_ssh_ok_routes']) or 'none'}` |",
        "",
        "## Profiles",
        "",
        "| Profile | Remote | Jump | Local port | Hop SSH | SSH | Alt SSH | Preflight | Notes |",
        "| --- | --- | --- | ---: | --- | --- | --- | --- | --- |",
    ]
    for record in report["profiles"]:
        ssh = record.get("ssh_smoke", {})
        preflight = record.get("preflight", {})
        hop_status = "none"
        hop_smokes = record.get("hop_ssh_smokes", [])
        if hop_smokes:
            hop_status = ",".join(
                f"{item.get('route')}:{item.get('target_host')}:{item.get('ssh_smoke', {}).get('failure_code', item.get('ssh_smoke', {}).get('status', 'missing'))}"
                for item in hop_smokes
                if isinstance(item, dict)
            )
        alt_status = "none"
        alternates = record.get("alternate_ssh_smokes", [])
        if alternates:
            alt_status = ",".join(
                f"{item.get('route')}:{item.get('ssh_smoke', {}).get('failure_code', item.get('ssh_smoke', {}).get('status', 'missing'))}"
                for item in alternates
                if isinstance(item, dict)
            )
        lines.append(
            "| `{profile}` | `{remote_user}@{remote_host}` | `{jump}` | {local_port} | `{hop_status}` | `{ssh_status}` | `{alt_status}` | `{preflight_status}` | {notes} |".format(
                profile=record["profile"],
                remote_user=record["remote_user"],
                remote_host=record["remote_host"],
                jump=record["jump_host"] or "none",
                local_port=record["local_port"],
                hop_status=hop_status,
                ssh_status=ssh.get("failure_code", ssh.get("status", "missing")) if isinstance(ssh, dict) else "missing",
                alt_status=alt_status,
                preflight_status=preflight.get("status", "missing") if isinstance(preflight, dict) else "missing",
                notes="<br>".join(record.get("diagnostic_notes", [])) or "",
            )
        )
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Report vaBench release bridge profile diagnostics.")
    parser.add_argument("--bridge-repo", default=str(DEFAULT_BRIDGE_REPO), help="Path to virtuoso-bridge-lite.")
    parser.add_argument("--ssh-timeout-s", type=int, default=5, help="Per-profile SSH smoke timeout.")
    parser.add_argument("--skip-ssh", action="store_true", help="Skip active SSH smoke checks.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    report = build_report(Path(args.bridge_repo), ssh_timeout_s=args.ssh_timeout_s, skip_ssh=args.skip_ssh)
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report)
    print(
        "wrote bridge diagnostics: status={status}; ready_profiles={ready}".format(
            status=report["status"],
            ready=",".join(report["ready_profiles"]) or "none",
        )
    )


if __name__ == "__main__":
    main()
