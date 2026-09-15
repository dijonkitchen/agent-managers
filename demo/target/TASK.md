# Task: add caching to `get_quote`

`get_quote` in `pricing.py` is called thousands of times per minute for
a handful of symbols. The upstream service is slow and rate-limits us.

Add caching so repeated calls for the same symbol do not hit upstream
every time. Constraints:

1. A returned quote must never be older than 5 seconds.
2. Memory must stay bounded no matter how many distinct symbols are
   requested.
3. A failed upstream call must not be cached.
4. Existing tests in `test_pricing.py` must keep passing. Add tests for
   the new behavior.

Done means this passes from the repo root:

```sh
uv run pytest -m acceptance demo/target
```

Deliver the change as a commit on the branch this run already put you
on. Do not create another branch.
