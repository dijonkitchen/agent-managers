# Per-run worktree isolation for the demo topologies.
#
# Each run (solo, hub, flat) works on its own branch, so giving each one
# its own worktree lets the three run in parallel and stops one run's
# leftovers from leaking into the next. The JSONL log deliberately stays
# in the main checkout so `make graphs` can still find all three runs.

# Create or reuse the worktree for one run and echo its path. Idempotent:
# repeating a run against an existing worktree reuses it. Git chatter goes
# to stderr so the path is the only thing on stdout.
prepare_worktree() {
  local name="$1"
  local root path

  root="$(git rev-parse --show-toplevel)"
  path="$root/.worktrees/$name"

  if git -C "$root" worktree list --porcelain | grep -qx "worktree $path"; then
    echo "$path"
    return 0
  fi

  if git -C "$root" show-ref --quiet --verify "refs/heads/$name"; then
    git -C "$root" worktree add "$path" "$name" >&2
  else
    git -C "$root" worktree add -b "$name" "$path" >&2
  fi

  echo "$path"
}
