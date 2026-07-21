from pathlib import Path


RUNTIME_DIR = Path(__file__).resolve().parents[2] / "public-agent-runtime"


def test_docker_build_context_is_allowlisted() -> None:
    dockerignore = (RUNTIME_DIR / ".dockerignore").read_text(encoding="utf-8")
    assert dockerignore.splitlines()[0] == "*"
    assert "!Dockerfile" in dockerignore
    assert "!requirements.lock" in dockerignore
    assert "!runtime/entrypoint.sh" in dockerignore


def test_runtime_image_is_pinned_and_non_root() -> None:
    dockerfile = (RUNTIME_DIR / "Dockerfile").read_text(encoding="utf-8")
    assert "FROM python:3.10.14-slim-bookworm@sha256:" in dockerfile
    assert "pip install --no-cache-dir --require-hashes" in dockerfile
    assert '"package_version"] == "0.8.3"' in dockerfile
    assert "USER 10001:10001" in dockerfile
    assert "COPY ." not in dockerfile


def test_launcher_exposes_only_public_runtime_mounts() -> None:
    launcher = (RUNTIME_DIR / "run.sh").read_text(encoding="utf-8")
    assert "--read-only" in launcher
    assert "--cap-drop=ALL" in launcher
    assert "--security-opt=no-new-privileges" in launcher
    assert '--user "$HOST_UID:$HOST_GID"' in launcher
    assert "--network=\"$NETWORK\"" in launcher
    assert launcher.count("--mount") == 3
    assert "dst=/workspace/public/task,readonly" in launcher
    assert "dst=/workspace/public/submission" in launcher
    assert "dst=/workspace/work" in launcher
    assert "benchmark" not in launcher.lower()
    assert "evaluator" not in launcher.lower()


def test_evas_and_all_dependencies_are_hash_locked() -> None:
    lock = (RUNTIME_DIR / "requirements.lock").read_text(encoding="utf-8")
    assert "evas-sim==0.8.3" in lock
    packages = [line for line in lock.splitlines() if line and not line[0].isspace() and "==" in line]
    assert packages
    for package in packages:
        assert package.endswith(" \\")
