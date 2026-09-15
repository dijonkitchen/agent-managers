"""Tests for demo/lib/worktree.sh, the per-run worktree helper.

Each topology run gets its own worktree so the three runs cannot fight
over one working tree. The helper has to be idempotent because a run is
often repeated against a worktree that already exists.
"""

import subprocess
from pathlib import Path

HELPER = Path(__file__).resolve().parents[2] / "demo" / "lib" / "worktree.sh"


def git(repo: Path, *args: str) -> str:
    out = subprocess.run(
        ["git", *args], cwd=repo, capture_output=True, text=True, check=True
    )
    return out.stdout.strip()


def prepare(repo: Path, name: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["bash", "-c", f'source "{HELPER}"; prepare_worktree {name}'],
        cwd=repo,
        capture_output=True,
        text=True,
    )


def make_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "t@example.com")
    git(repo, "config", "user.name", "t")
    (repo / "TASK.md").write_text("task\n")
    git(repo, "add", "TASK.md")
    git(repo, "commit", "-qm", "init")
    return repo


def test_creates_a_worktree_and_branch_named_for_the_run(tmp_path):
    repo = make_repo(tmp_path)
    result = prepare(repo, "flat")
    assert result.returncode == 0, result.stderr
    path = Path(result.stdout.strip())
    assert path == repo / ".worktrees" / "flat"
    assert (path / "TASK.md").exists()
    assert "flat" in git(repo, "branch", "--format=%(refname:short)").splitlines()


def test_is_idempotent_so_a_run_can_be_repeated(tmp_path):
    repo = make_repo(tmp_path)
    first = prepare(repo, "hub")
    second = prepare(repo, "hub")
    assert second.returncode == 0, second.stderr
    assert first.stdout.strip() == second.stdout.strip()


def test_reuses_an_existing_branch_instead_of_failing(tmp_path):
    repo = make_repo(tmp_path)
    git(repo, "branch", "solo")
    result = prepare(repo, "solo")
    assert result.returncode == 0, result.stderr
    path = Path(result.stdout.strip())
    assert git(path, "rev-parse", "--abbrev-ref", "HEAD") == "solo"


def test_prints_only_the_path_on_stdout(tmp_path):
    repo = make_repo(tmp_path)
    result = prepare(repo, "flat")
    assert result.stdout.strip().count("\n") == 0
    assert result.stdout.strip().endswith("/.worktrees/flat")
