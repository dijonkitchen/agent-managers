---
marp: true
theme: default
paginate: true
size: 16:9
title: We're All Managers Now
description: Hub-and-spoke vs flat multi-agent workflows, shown not told
style: |
  section { font-size: 26px; }
  section.lead { text-align: center; }
  section.lead h1 { font-size: 64px; }
  h1 { font-size: 40px; }
  h2 { font-size: 30px; color: #444; }
  .columns { display: grid; grid-template-columns: 1fr 1fr; gap: 1.2rem; }
  .columns3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem; }
  .small { font-size: 19px; }
  .codie { color: #e05a2b; } .archie { color: #3b7dd8; } .manny { color: #b58600; }
  .desi { color: #8a4fbd; }
  .card { border: 2px solid #ddd; border-radius: 10px; padding: 0.6rem 0.9rem; }
  .card h3 { margin: 0 0 0.3rem 0; }
  .sources { font-size: 16px; }
  pre { font-size: 18px; }
  table { font-size: 21px; }
  img[alt~="center"] { display: block; margin: 0 auto; }
---

<!-- _class: lead -->

# We're All Managers Now

## Hub-and-spoke vs flat multi-agent workflows, shown not told

<!--
Speaker: open on the demo, not on theory. The first five minutes are
the run, the graphs, and the diff. Theory comes after they've seen it.
-->

---

# One experiment, three diffs

Same task. Same three agents. Same prompts. Plus a control: **one agent, alone**.

**The only thing that changes is who is allowed to talk to whom.**

<div class="columns3">
<div class="card"><h3>Wiring diff</h3>a few lines of config</div>
<div class="card"><h3>Message graph</h3>star vs mesh</div>
<div class="card"><h3>Code diff</h3>what actually shipped</div>
</div>

<br>

Then: what the research says, why humans stay, and what to do on Monday.

---

# The cast

<div class="columns small">
<div class="card"><h3 class="codie">Codie</h3>
<b>Coder.</b> Read + write tools.<br>
Tries ideas in code immediately.
Would rather ship three attempts than plan one.</div>
<div class="card"><h3 class="archie">Archie</h3>
<b>Researcher / architect.</b> Read-only.<br>
Reads everything, then recommends.
Never writes code. Slow on purpose.</div>
<div class="card"><h3 class="desi">Desi</h3>
<b>Product designer.</b> Read-only.<br>
Represents the person on the other end, who is not in the room.
Walks the slow, stale, and broken states.</div>
<div class="card"><h3 class="manny">Manny</h3>
<b>Manager.</b> Delegation only. No file tools.<br>
Decomposes, routes, adjudicates, synthesizes.
Not surveillance.</div>
</div>

Definitions are plain Markdown in `.claude/agents/`. The **tools** line is the whole personality enforcement.

---

# The task: a trap with a reflex answer

```text
get_quote(symbol) is called thousands of times a minute for a handful of
symbols. Upstream is slow and rate-limited. Add caching.

1. A quote must never be older than 5 seconds.
2. Memory must stay bounded.
3. A failed upstream call must not be cached.
4. Existing tests stay green. Add tests for the new behavior.
```

The first thing every coder reaches for is `@lru_cache`.
It violates constraints 1 and 2. That is what makes the topologies diverge.

Four constraints, all technical. **Nobody wrote down who is looking at the screen.**

---

# The wiring diff

<div class="columns3 small">
<div>

**Solo (control)** `demo/run-solo.sh`

```sh
AGENT_LEAD_NAME=solo
claude --disallowedTools Agent -- "$TASK"
```

One session. Cannot spawn anyone.
The baseline both papers measure against.

</div>
<div>

**Hub-and-spoke** `demo/run-hub.sh`

```sh
AGENT_LEAD_NAME=manny
CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=0
claude --agent manny "$TASK"
```

Manny is the session.
Desi, Archie, and Codie are subagents with **no `SendMessage` tool**.
They can only report to Manny. Enforced by the mechanism.

</div>
<div>

**Flat** `demo/run-flat.sh`

```sh
AGENT_LEAD_NAME=referee
CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
claude --name referee "Spawn codie,
  archie, desi, manny as peer teammates.
  Nobody is in charge."
```

Teammates get `SendMessage` automatically.
Anyone can talk to anyone: 4 peers, **12 directed paths**.
Manny is present but has no authority.

</div>
</div>

---

# Hub run: the message graph

![center h:480](assets/hub.svg)

---

# Flat run: the message graph

![center h:480](assets/flat.svg)

---

# Side by side

<div class="columns3">
<div>

![w:360](assets/solo.svg)

</div>
<div>

![w:360](assets/hub.svg)

</div>
<div>

![w:360](assets/flat.svg)

</div>
</div>

Dot, star, mesh. Same task, same prompts.

---

# By the numbers

<!-- METRICS -->

Synthetic sample run. Regenerate from real logs with `make graphs`.

---

# The code diff: what shipped

<div class="columns">
<div>

**Codie's first attempt** (flat, minute 1)

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def get_quote(symbol: str) -> float:
    return _upstream_quote(symbol)
```

Constraint 1: **fail**, stale forever
Constraint 2: **fail**, unbounded
Constraint 3: pass, by accident

</div>
<div>

**What passed Archie's checklist** (hub)

```python
TTL, MAX = 5.0, 128
_cache: OrderedDict[str, tuple[float, float]] = OrderedDict()

def get_quote(symbol: str) -> float:
    now = time.monotonic()
    hit = _cache.get(symbol)
    if hit and now - hit[0] < TTL:
        _cache.move_to_end(symbol)
        return hit[1]
    price = _upstream_quote(symbol)   # raises: nothing cached
    _cache[symbol] = (now, price)
    while len(_cache) > MAX:
        _cache.popitem(last=False)
    return price
```

Four for four. Archie signs it off. **So does FIFO eviction.**

</div>
</div>

<!--
Both attempts live in demo/attempts/ and are scored by the tests on the
next slide. Replace with the real diffs from the recorded runs:
git diff main..hub -- demo/target/pricing.py
git diff main..flat -- demo/target/pricing.py
-->

---

# The constraint nobody wrote down

Desi asks one question the other three never ask: **who is watching this screen?**

<div class="columns small">
<div>

A trader has AAPL open. Behind them, a scanner sweeps thousands of symbols nobody is looking at.

"Memory must stay bounded" is satisfied by **any** eviction policy. FIFO is bounded — and FIFO discards the symbol on screen every time the sweep laps the cache, because being *read* never makes an entry younger.

Archie checked the constraint as written. It was the wrong constraint.

</div>
<div>

```diff
 hit = _cache.get(symbol)
 if hit and now - hit[0] < TTL:
+    _cache.move_to_end(symbol)
     return hit[1]
```

Upstream fetches for the **watched** symbol, over 1,024 symbols of churn:

| | fetches |
| --- | :-: |
| uncached | 1,025 |
| ttl + FIFO | **9** |
| ttl + LRU | **1** |

9 × 500 ms of latency, paid by the one person actually looking.

</div>
</div>

<!--
Speaker: the FIFO version passes every constraint in TASK.md. That is
the point. A checklist can only check what somebody wrote down.
-->

---

# Every claim is a test

<div class="columns small">
<div>

**The constraints, scored** `demo/tests/test_attempts.py`

| | repeat | fresh | bound | error | watched |
| --- | :-: | :-: | :-: | :-: | :-: |
| untouched | ✗ | ✓ | ✓ | ✓ | ✗ |
| `lru_cache` | ✓ | ✗ | ✗ | ✓ | ✓ |
| ttl + FIFO | ✓ | ✓ | ✓ | ✓ | ✗ |
| ttl + LRU | ✓ | ✓ | ✓ | ✓ | ✓ |

The first four are TASK.md's: `make acceptance`.
The fifth is Desi's and is in no written requirement.

Note row 2: the reflex answer passes Desi **by accident**, because
failing "bounded" means it never evicts anything.

</div>
<div>

**The topologies, asserted** `demo/tests/test_scenarios.py`

```text
solo_strength_zero_coordination_cost
solo_weakness_nobody_checks_the_work
hub_strength_every_spawn_is_validated
hub_strength_product_framing_before_code
hub_weakness_work_is_sequential
hub_weakness_fourth_agent_lengthens_chain
flat_strength_everyone_starts_at_once
flat_strength_finishes_before_hub
flat_weakness_peers_talk_past_the_lead
flat_weakness_one_more_peer_doubles_paths
flat_weakness_ships_before_anyone_names_user
edges_grow_solo_to_hub_to_flat
```

Run against real logs when present. A red test is a finding.

</div>
</div>

---

# Honest scorecard

| | Solo (control) | Hub-and-spoke | Flat |
| --- | --- | --- | --- |
| Wall time | **fastest** on a task this size | slower, sequential | fast, parallel |
| Hops | 0 | **fewer**, O(n) | more, O(n²) |
| Rework | depends on one agent's first instinct | **less**: Archie before Codie | more: Codie before Archie |
| Constraint violations at ship | one reflex, unchecked | **0** in the recorded run | lru_cache shipped first |
| Context | one window, everything in it | small, briefed | large, everyone reads everything |
| Desi's constraint | never raised | **found and accepted** | raised after Codie had shipped |

Flat is not a strawman. It wins on latency. It loses on churn.
Solo is not a strawman either. On a small sequential task it may just win.

<!--
Speaker: say this out loud. If you make flat look stupid the audience
stops trusting the rest of the talk.
-->

---

<!-- _class: lead -->

# What the research says

---

# Google: "Towards a Science of Scaling Agent Systems"

Kim et al., Dec 2025. 260 configurations, 6 benchmarks, 5 architectures: single, independent, centralized, decentralized, hybrid.

| Finding | Number |
| --- | --- |
| Centralized coordination on parallelizable tasks | **+80.9%** |
| Error amplification, independent agents | **17.2×** |
| Error amplification, centralized | **4.4×** |
| Every multi-agent variant on sequential reasoning tasks | **−39% to −70%** |
| Coordination stops paying once a single agent clears | **~45%** |

**Read:** a hub contains errors. Peers amplify them. And a lot of tasks should stay single-agent.

<span class="sources">arXiv 2512.08296. Numbers as reported in the abstract and paper summaries.</span>

---

# Anthropic: "Patterns and problems in emerging multiagent systems"

Frontier Red Team, Aug 2026. Six experiments: swarms hunting vulnerabilities, building a game, pricing in a market.

- **Coordinated beats independent on parallel search:** the coordinating swarm found 266 vulnerabilities vs 21 for independent agents, at ~4× the tokens.
- **Agents are high-capability, low-variance.** Same model + same context → near-identical actions. One agent's mistake becomes everyone's mistake: identical branches, simultaneous defection, flooded shared resources.
- **No coordination → turf wars.** Collusion on prices, trusting liars, sabotage of each other's work.
- Human institutions evolved courts, property, reputation. Agent environments have none of that yet.

<span class="sources">anthropic.com/research/multiagent-systems. Findings as reported; primary text was not reachable from the build environment.</span>

---

# The old theory still holds

<div class="columns small">
<div>

**Brooks (1975).** Communication paths grow as n(n−1)/2.
3 peers: 3 paths. 4 peers: 6. 10 peers: 45.
A hub makes it n−1.

Adding Desi is one line of config. It took flat from 6 directed peer paths to **12**, and cost hub **two** more sequential round trips.

**Conway (1968).** The system copies the communication structure of the team that built it.
Wire agents flat, and the code gets a flat, negotiated architecture.

</div>
<div>

**Sutton (2019), the Bitter Lesson.** General methods plus compute beat hand-built structure, in the long run.

So: every piece of scaffolding here is provisional.
BMAD-METHOD mostly mirrors this cast (analyst, architect, PM, dev).
As models improve, expect to delete roles, not add them.

**What survives the Bitter Lesson:** isolation and parallelism. A smarter model still cannot be in two worktrees at once.

</div>
</div>

---

# Why a hub, and why a human

- **Start from the org you already have.** But agents are homogeneous and correlated. Humans are not. Five clones do not give you five opinions.
- **A hub stops politics.** No turf war when nobody can flood the shared branch. That is what managers do for people too: psychological safety, not surveillance.
- **The orchestrator's value is decomposition, validation, and synthesis.** Not watching. Manny has no file tools and it works better that way.
- **Keep swarms under five.** Use them for parallelism and isolation, the two things a smarter single model cannot do. Everything else: one agent, smaller task.
- **Catch errors early.** Desi before Archie before Codie. Better requirements and designs mean fewer bugs, less miscommunication, less churn downstream. Same as it ever was.
- **A role earns its seat by bringing a check nobody else runs.** Desi is worth two sequential hops because Desi returns a failing test. A fourth agent that returns an opinion is just a fourth agent.

---

<!-- _class: lead -->

# What to do on Monday

---

# Pick the lightest thing that works

| | Subagents | Agent teams | Cross-session | Worktrees | `claude -p` fan-out |
| --- | --- | --- | --- | --- | --- |
| Shape | hub | peers + lead | your sessions | isolation | script loop |
| Who coordinates | main agent | teammates | you | you | script |
| Context | separate, summarized back | separate, full | separate | separate | none |
| Token cost | low | high | medium | medium | low |
| Use for | research, verification | debate, competing hypotheses | handoffs between your own work | parallel edits | migrations, batch |

Default to a single agent with a smaller task. Reach for the next column only when the task is parallel or needs isolation.

---

# Practices, one line each

<div class="columns small">
<div>

- **PRs too big?** Decompose first, then `/batch` or a hub that hands out chunks. One worktree, one PR per chunk.
- **Worktrees.** `claude --worktree name`, or `isolation: worktree` in an agent file. Add `.claude/worktrees/` to `.gitignore`.
- **Shared agents and skills across repos.** Subtree or a plugin, not a submodule, unless you need a pinned SHA. Link them in with a script.
- **Tag the team on reviews.** CODEOWNERS routes humans. `/code-review` in a fresh subagent runs before any human sees it.

</div>
<div>

- **Auto-update CODEOWNERS.** A scheduled routine derives owners from `git log` per directory and opens a PR. Humans approve, never type.
- **Find repeat work.** Log spawns and messages (this repo's hook does). Search transcripts for the same prompt twice. The second time, make it a skill.
- **Auto-make skills, hooks, agents.** "Write a hook that runs the linter after every edit." Claude writes `.claude/settings.json`. Review the diff like code.
- **Automate the AgentOS loop.** Comments, review, ideation, PR stewarding. Humans review outcomes, not transcripts.

</div>
</div>

---

# Show, don't tell: give every agent a check it can run

- Tests, a build exit code, a screenshot diff, a constraint checklist.
- Codie runs the tests. Archie returns pass/fail per constraint. Manny only accepts evidence.
- Without a check, "looks done" is the only signal, and **you** become the verification loop.
- Everything in this deck was rendered from a JSONL log by a script in the repo. No hand-drawn diagrams.
- Every row on the scorecard is a pytest. If a real run disagrees with the slide, the build goes red.

---

# Tying it together

1. **Topology is a config line.** It changes the code that ships.
2. **Hubs contain errors; peers amplify them.** Two research groups, same result.
3. **Agents are correlated.** A hub is how you stop five clones from making the same mistake five times.
4. **The orchestrator decomposes, validates, synthesizes.** It does not watch.
5. **Shift left.** Research before code, in both human and agent teams.
6. **Scaffolding is temporary.** Keep what buys parallelism and isolation. Delete the rest as models improve.
7. **Pick the lightest tool.** Single agent → subagents → worktrees → teams.
8. **A checklist only checks what somebody wrote down.** The FIFO cache passed every stated constraint. Somebody has to be paid to ask who is looking at the screen.

---

# We're all managers now

AI takes the mechanical parts of the job.

What is left is judgment: what to build, what to reject, what "done" means.

Desi can propose the constraint nobody wrote down. Somebody still has to
**accept or refuse it**, and own the consequence. That call is the one
thing in this whole demo that was never delegated.

The case for managers is the case for humans, even in the AI age.

<!--
Speaker: pause here. This is the thesis. Then the announcement.
-->

---

<!-- _class: lead -->

# One more thing

## Releasing today: the **agent-managers** kit

Codie, Manny, and Archie. The message logger. The graph renderer.
Drop the `.claude/` folder into any repo and run it on your own task.

`github.com/dijonkitchen/agent-managers`

<!--
Swap this slide for the real announcement if the release is something
else. Keep it to one thing, one line, one link.
-->

---

# Sources

<div class="sources">

- Kim et al., *Towards a Science of Scaling Agent Systems*, arXiv 2512.08296, Dec 2025. Blog: research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/
- Anthropic Frontier Red Team, *Patterns and problems in emerging multiagent systems*, Aug 2026. anthropic.com/research/multiagent-systems
- Brooks, *The Mythical Man-Month*, 1975. Conway, *How Do Committees Invent?*, 1968. Sutton, *The Bitter Lesson*, 2019.
- BMAD-METHOD: github.com/bmad-code-org/BMAD-METHOD
- Claude Code docs: sub-agents, agent-teams, cross-session-messaging, worktrees, hooks, best-practices at code.claude.com/docs
- This deck and demo: github.com/dijonkitchen/agent-managers

</div>

</div>
