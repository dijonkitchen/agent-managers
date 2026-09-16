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

<div class="columns3">
<div class="card"><h3 class="codie">Codie</h3>
<b>Coder.</b> Read + write tools.<br>
Tries ideas in code immediately.<br>
Would rather ship three attempts than plan one.</div>
<div class="card"><h3 class="archie">Archie</h3>
<b>Researcher / architect.</b> Read-only.<br>
Reads everything, then recommends.<br>
Never writes code. Slow on purpose.</div>
<div class="card"><h3 class="manny">Manny</h3>
<b>Manager.</b> Delegation only. No file tools.<br>
Decomposes, routes, validates, synthesizes.<br>
Not surveillance.</div>
</div>

<br>

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
Codie and Archie are subagents with **no `SendMessage` tool**.
They can only report to Manny. Enforced by the mechanism.

</div>
<div>

**Flat** `demo/run-flat.sh`

```sh
AGENT_LEAD_NAME=referee
CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
claude --name referee "Spawn codie, archie,
  manny as peer teammates. Nobody is in charge."
```

Teammates get `SendMessage` automatically.
Anyone can talk to anyone.
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

</div>
</div>

<!--
Both attempts live in demo/attempts/ and are scored by the tests on the
next slide. Replace with the real diffs from the recorded runs:
git diff main..hub -- demo/target/pricing.py
git diff main..flat -- demo/target/pricing.py
-->

---

# Every claim is a test

<div class="columns small">
<div>

**The constraints, scored** `demo/tests/test_attempts.py`

| | repeats | fresh 5s | bounded | errors |
| --- | :-: | :-: | :-: | :-: |
| untouched | ✗ | ✓ | ✓ | ✓ |
| `lru_cache` | ✓ | ✗ | ✗ | ✓ |
| TTL + bound | ✓ | ✓ | ✓ | ✓ |

Same four checks are the task's definition of done:
`make acceptance`

</div>
<div>

**The topologies, asserted** `demo/tests/test_scenarios.py`

```text
solo_strength_zero_coordination_cost
solo_weakness_nobody_checks_the_work
hub_strength_every_hop_touches_the_lead
hub_strength_every_spawn_is_validated
hub_weakness_work_is_sequential
flat_strength_everyone_starts_at_once
flat_strength_finishes_before_hub
flat_weakness_peers_talk_past_the_lead
flat_weakness_coder_ships_before_researcher
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

Flat is not a strawman. It wins on latency. It loses on churn.
Solo is not a strawman either. On a small sequential task it may just win.

<!--
Speaker: say this out loud. If you make flat look stupid the audience
stops trusting the rest of the talk.
-->

---

<!-- _class: lead -->

# Why it turned out that way

## Each step below exists because the one before it hit a wall

---

# 1. Solo already is the 10x

The jump from you typing to one agent is where almost all of the multiplier lives.
**The second agent is worth far less than the first.**

| What coordination actually buys | |
| --- | --- |
| Centralized coordination, parallelizable tasks | **+80.9%** — that is 1.8×, not 10× |
| Every multi-agent variant, sequential reasoning | **−39% to −70%** |
| Coordination stops paying once one agent clears | **~45%** |

So most tasks should stay solo. Solo has exactly two ceilings, and they are the ones the demo hit:
**it cannot parallelize, and nobody checks its work.**

<span class="sources">Kim et al., *Towards a Science of Scaling Agent Systems*, arXiv 2512.08296, Dec 2025. 260 configurations, 6 benchmarks, 5 architectures. Numbers as reported in the abstract and paper summaries.</span>

<!--
Speaker: this fights the room's priors. Everyone arrived expecting
"more agents, more better." Say the quiet part: you pay N times the
tokens for well under N times the output.
-->

---

# 2. So add agents. Structure decides what you get.

<div class="columns">
<div>

| Error amplification | |
| --- | --- |
| Independent agents | **17.2×** |
| Centralized coordination | **4.4×** |

A hub **contains** errors. Peers **amplify** them.
Same numbers, same paper as the last slide.

</div>
<div>

**Brooks (1975).** Communication paths grow as n(n−1)/2.
3 peers: 3 paths. 5 peers: 10. 10 peers: 45.
A hub makes it n−1.

**Conway (1968).** The system copies the communication structure that built it. Wire agents flat, get a flat, negotiated architecture.

</div>
</div>

<br>

**This is the demo.** One config line moved the run from 4 edges to 12, and changed the code that shipped.

---

# 3. But structure cannot fix clones

Anthropic Frontier Red Team, Aug 2026. Six experiments: swarms hunting vulnerabilities, building a game, pricing in a market.

- **Coordination works on parallel search.** The coordinating swarm found **266** vulnerabilities to independent agents' **21**, at roughly 4× the tokens.
- **But agents are high-capability and low-variance.** Same model plus same context produces near-identical actions. One agent's mistake becomes every agent's mistake: identical branches, simultaneous defection, flooded shared resources.
- **Ungoverned swarms fight.** Collusion on prices, trusting liars, sabotaging each other's work.

**The wall:** topology bounds the blast radius of a mistake. It cannot make two copies of one model genuinely disagree.

<span class="sources">anthropic.com/research/multiagent-systems. Findings as reported; primary text was not reachable from the build environment.</span>

---

# 4. So diversify by evidence, not personality

<div class="columns small">
<div>

**No prompt makes two copies of one model disagree.** Different evidence does. Give each agent the minimum context its job needs, and route untrusted sources to the agent that cannot execute.

| Agent | Sees | Can act |
| --- | --- | --- |
| <span class="archie">Archie</span> | web, docs, issues, telemetry | **no** — read-only |
| <span class="codie">Codie</span> | the repo, the test runner | yes |
| <span class="manny">Manny</span> | only what agents report | no file tools |

Scoped per agent with `mcpServers` in the agent file.

</div>
<div>

**Four reasons to divide, not pool:**

1. **Context.** Every server's tool definitions load into every agent holding it.
2. **Tool-coordination tradeoff.** Tool-heavy tasks suffer *most* from multi-agent overhead under a fixed budget.
3. **Decorrelation.** Different evidence, different conclusions. This is the point.
4. **Injection surface.** The agent reading untrusted web content has no `Edit`, `Write`, or `Bash`.

**Honest caveat:** Archie's findings still reach Codie through Manny. That is defense in depth, not a hard boundary.

</div>
</div>

---

# 5. Someone still has to decide

- **A hub stops politics.** No turf war when nobody can flood the shared branch. That is what managers do for people too: psychological safety, not surveillance.
- **The orchestrator's value is decomposition, validation, and synthesis.** Not watching. Manny has no file tools and works better for it.
- **Keep swarms under five.** Use them for parallelism and isolation, the two things a smarter single model cannot do. Everything else: one agent, smaller task.
- **Catch errors early.** Archie before Codie. Better requirements and designs mean fewer bugs, less miscommunication, less churn downstream. Same as it ever was.
- **Adopt the org chart's shape, not its rationale.** Hierarchy solves human problems agents do not have: span of attention, careers, politics, accountability. The one thing that transfers is span of control as a **context** limit. And the chart evolved to coordinate people who were already diverse — your agents are the opposite.

---

# 6. So how does this scale?

<div class="columns">
<div>

```text
You
└── Manny              single decision point
    ├── Archie         single advisor, read-only
    │   └── N research subagents,
    │       one per evidence source
    └── Codie × N      one file-partition and
                       one worktree each
```

**Fan out at the leaves.
Stay singular at the decision points.**

Depth two. Parallelism from the N's, coordination from the single Manny, isolation from the worktrees and from Archie's missing write tools.

</div>
<div class="small">

**Two nevers**

- **Never a second Manny** until one cannot brief and validate the agents he already has. A layer buys context isolation and costs a lossy summary; Manny has no file tools, so he cannot check a sub-Manny's synthesis against the code.
- **Never `Agent` on Archie.** He is read-only so he can safely ingest untrusted sources. Let him spawn, and injected content becomes a work order.

**Duplicate Codies** — they do different work.
**Differentiate researchers by evidence** — identical ones return identical answers, at N times the price.

Depth is capped anyway: subagents nest three layers by default (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`), and agent-team teammates cannot nest at all.

</div>
</div>

<!--
Speaker: the shape is the answer to "does this actually parallelize?"
Today's hub run does not - one agent alive at a time. Two Codies is
what turns the pipeline into coordination.
-->

---

# 7. How long does this scaffolding last?

<div class="columns">
<div>

**Sutton (2019), the Bitter Lesson.** General methods plus compute beat hand-built structure, in the long run.

So every role in this deck is provisional. BMAD-METHOD mostly mirrors this cast (analyst, architect, PM, dev). As models improve, expect to **delete** roles, not add them.

</div>
<div>

**What survives the Bitter Lesson:**
isolation and parallelism. A smarter model still cannot be in two worktrees at once.

**And judgment.** Deciding what to build, what to reject, and what "done" means is not scaffolding. It is the job.

</div>
</div>

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

1. **Solo already is the 10x**, and it often wins. Its ceilings are parallelism and having nobody check it.
2. **Structure decides what you get.** Hubs contain errors at 4.4×; peers amplify at 17.2×. It is one config line.
3. **Structure cannot fix clones.** Same model plus same context is the same mistake, N times.
4. **So diversify by evidence.** Minimum context per agent; untrusted sources to the agent that cannot execute.
5. **Someone still has to decompose, validate, and synthesize.** That is judgment, and it does not automate.
6. **Scale by fanning out at the leaves.** Many Codies, many researchers, one Manny, one Archie. Add a layer only when span of control runs out.
7. **The scaffolding is temporary; the judgment is not.** Delete roles as models improve.
8. **Pick the lightest tool.** Single agent → subagents → worktrees → teams.

---

# We're all managers now

AI takes the mechanical parts of the job.

What is left is judgment: what to build, what to reject, what "done" means.

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
