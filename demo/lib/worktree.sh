# Per-run worktree isolation for the demo topologies.
#
# Each run (solo, hub, flat) works on its own branch, so giving each one
# its own worktree lets the three run in parallel and stops one run's
# leftovers from leaking into the next. The JSONL log deliberately stays
# in the main checkout so `make graphs` can still find all three runs.

# The main checkout, even when called from inside a linked worktree: the
# per-worktree git dirs live under the main checkout's .git directory.
# Without this, rehearsing a run from inside .worktrees/ would nest a
# worktree inside a worktree.
main_checkout() {
  dirname "$(git rev-parse --path-format=absolute --git-common-dir)"
}

# Create a worktree for one run and echo its path. The name carries a
# timestamp rather than being just the run name: a rehearsal repeats a
# run many times, and a fixed name collides with the branch and the
# worktree the previous run left behind. The directory name doubles as
# the branch name, so a run script can name the branch in its prompt.
prepare_worktree() {
  local run="$1" root base name path n=2

  root="$(main_checkout)"
  base="$run-$(date -u +%Y%m%d-%H%M%S)"
  name="$base"
  while [ -e "$root/.worktrees/$name" ] ||
    git -C "$root" show-ref --quiet --verify "refs/heads/$name"; do
    name="$base-$n"
    n=$((n + 1))
  done

  path="$root/.worktrees/$name"
  # Explicit HEAD: every run starts from the main checkout's current
  # commit, never from whatever an earlier run's worktree sits on.
  git -C "$root" worktree add -b "$name" "$path" HEAD >&2
  echo "$path"
}
