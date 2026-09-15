"""Tests for demo/lib/worktree.sh, the per-run worktree helper.

Each topology run gets its own worktree on its own branch. The names are
generated per run rather than fixed, because a rehearsal repeats a run
many times and a fixed name collides with whatever the last run left
behind -- including a worktree for that branch parked somewhere else.
"""

import re
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
        ["bash", "-c", f'set -euo pipefail; source "{HELPER}"; prepare_worktree {name}'],
        cwd=repo,
        capture_output=True,
        text=True,
    )


def prepared_path(repo: Path, name: str) -> Path:
    result = prepare(repo, name)
    assert result.returncode == 0, result.stderr
    return Path(result.stdout.strip())


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


def test_creates_a_worktree_on_a_branch_named_for_the_run(tmp_path):
    repo = make_repo(tmp_path)
    path = prepared_path(repo, "flat")
    assert path.parent == repo / ".worktrees"
    assert re.fullmatch(r"flat-\d{8}-\d{6}", path.name), path.name
    assert (path / "TASK.md").exists()
    # The worktree directory name is the branch name, so a run script can
    # tell its agents which branch they are on without a second lookup.
    assert git(path, "rev-parse", "--abbrev-ref", "HEAD") == path.name


def test_repeated_runs_get_their_own_worktree_and_branch(tmp_path):
    repo = make_repo(tmp_path)
    first = prepared_path(repo, "hub")
    second = prepared_path(repo, "hub")
    assert first != second
    branches = git(repo, "branch", "--format=%(refname:short)").splitlines()
    assert first.name in branches and second.name in branches
    worktrees = git(repo, "worktree", "list", "--porcelain")
    assert f"worktree {first}" in worktrees
    assert f"worktree {second}" in worktrees


def test_ignores_a_worktree_an_earlier_run_parked_elsewhere(tmp_path):
    """The failure that motivated this: `hub` checked out at another path."""
    repo = make_repo(tmp_path)
    git(repo, "worktree", "add", "-q", "-b", "hub", str(tmp_path / "elsewhere"))
    path = prepared_path(repo, "hub")
    assert path.parent == repo / ".worktrees"


def test_runs_from_inside_another_worktree_stay_in_the_main_checkout(tmp_path):
    repo = make_repo(tmp_path)
    inner = prepared_path(repo, "solo")
    (repo / "TASK.md").write_text("task v2\n")
    git(repo, "commit", "-qam", "second")

    path = prepared_path(inner, "hub")
    assert path.parent == repo / ".worktrees"
    # Based on the main checkout's HEAD, not on the stale worktree we ran from.
    assert git(path, "rev-parse", "HEAD") == git(repo, "rev-parse", "HEAD")


def test_prints_only_the_path_on_stdout(tmp_path):
    repo = make_repo(tmp_path)
    result = prepare(repo, "flat")
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip().count("\n") == 0
