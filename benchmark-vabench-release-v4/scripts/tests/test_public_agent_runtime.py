from pathlib import Path
import unittest


RUNTIME_DIR = Path(__file__).resolve().parents[2] / "public-agent-runtime"
REPO_ROOT = Path(__file__).resolve().parents[3]
ENVIRONMENT_DIR = REPO_ROOT / "environment"


class PublicAgentRuntimeTest(unittest.TestCase):
    def test_docker_build_context_is_allowlisted(self) -> None:
        dockerignore = (ENVIRONMENT_DIR / ".dockerignore").read_text(encoding="utf-8")
        self.assertEqual(dockerignore.splitlines()[0], "*")
        self.assertIn("!Dockerfile", dockerignore)
        self.assertIn("!requirements.lock", dockerignore)
        self.assertIn("!runtime/entrypoint.sh", dockerignore)

    def test_runtime_image_is_pinned_and_non_root(self) -> None:
        dockerfile = (ENVIRONMENT_DIR / "Dockerfile").read_text(encoding="utf-8")
        self.assertIn("FROM python:3.10.14-slim-bookworm@sha256:", dockerfile)
        self.assertIn("pip install --no-cache-dir --require-hashes", dockerfile)
        self.assertIn('"package_version"] == "0.8.3"', dockerfile)
        self.assertIn("USER 10001:10001", dockerfile)
        self.assertNotIn("COPY .", dockerfile)

    def test_launcher_exposes_only_public_runtime_mounts(self) -> None:
        launcher = (RUNTIME_DIR / "run.sh").read_text(encoding="utf-8")
        self.assertIn("--read-only", launcher)
        self.assertIn("--cap-drop=ALL", launcher)
        self.assertIn("--security-opt=no-new-privileges", launcher)
        self.assertIn('--user "$HOST_UID:$HOST_GID"', launcher)
        self.assertIn("--network=\"$NETWORK\"", launcher)
        self.assertEqual(launcher.count("--mount"), 3)
        self.assertIn("dst=/workspace/public/task,readonly", launcher)
        self.assertIn("dst=/workspace/public/submission", launcher)
        self.assertIn("dst=/workspace/work", launcher)
        self.assertNotIn("benchmark", launcher.lower())
        self.assertNotIn("evaluator", launcher.lower())

    def test_evas_and_all_dependencies_are_hash_locked(self) -> None:
        lock = (ENVIRONMENT_DIR / "requirements.lock").read_text(encoding="utf-8")
        self.assertIn("evas-sim==0.8.3", lock)
        packages = [
            line
            for line in lock.splitlines()
            if line and not line[0].isspace() and "==" in line
        ]
        self.assertTrue(packages)
        for package in packages:
            self.assertTrue(package.endswith(" \\"))


if __name__ == "__main__":
    unittest.main()
