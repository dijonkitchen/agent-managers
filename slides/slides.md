---
marp: true
theme: default
paginate: true
size: 16:9
title: Surviving the AI Age
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
  .scratched { font-size: 38px; font-weight: 700; color: #b0b0b0;
    text-decoration: line-through; text-decoration-color: #d64545;
    text-decoration-thickness: 4px; line-height: 1.3; }
  .byline { margin-top: 1.8rem; font-size: 24px; color: #555; }
  section.lead h1 .title { font-size: 52px; line-height: 1.15; }
  .figsplit { display: grid; grid-template-columns: 2.5fr 1fr; gap: 1.2rem; align-items: center; }
  .figure { text-align: center; }
  .figure .cap { font-size: 16px; color: #666; line-height: 1.35; }
  .qa { text-align: center; }
  .qa svg { display: block; margin: 0 auto 0.4rem; }
  .qa .seed { font-size: 30px; font-weight: 700; color: #2d3b4e; }
  .qa .caption { font-size: 22px; color: #666; margin-top: 0.2rem; }
  pre { font-size: 18px; }
  table { font-size: 21px; }
  img[alt~="center"] { display: block; margin: 0 auto; }
---

<!-- _class: lead -->

<div class="scratched">Multi-Agent Structure</div>
<div class="scratched">Agent Optimization Science</div>

# <span class="title">How to survive the AI age as an engineer</span>

<div class="byline">JC &middot; 2026-09-17</div>

<!--
Speaker: let the two crossed-out titles sit for a beat. The joke is that
the honest title is the one nobody would put on a conference abstract.
Open on the demo, not on theory. The first five minutes are the run,
the graphs, and the diff. Theory comes after they've seen it.

Do not answer the title here. The closing slide answers it, and the
answer is that you don't stay one.
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

Manny is the session and can resume Codie and Archie by name.
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
TTL_SECONDS = 5.0
MAX_ENTRIES = 128

_cache: "OrderedDict[str, tuple[float, float]]" = OrderedDict()
_lock = threading.Lock()

def get_quote(symbol: str) -> float:
    now = time.monotonic()

    with _lock:
        hit = _cache.get(symbol)
        if hit is not None and 0.0 <= now - hit[0] < TTL_SECONDS:
            _cache.move_to_end(symbol)  # read counts as recency
            return hit[1]

    # Outside the lock and before any mutation: if this raises, nothing was
    # ever written, so a failure is never cached.
    price = _upstream_quote(symbol)

    with _lock:
        # `now` is read before the fetch, so an entry is treated as older
        # than it is -- conservative on the freshness guarantee.
        _cache[symbol] = (now, price)
        _cache.move_to_end(symbol)  # assigning an existing key does not reorder
        while len(_cache) > MAX_ENTRIES:
            _cache.popitem(last=False)

    return price
```

Verbatim from `1bca134`.

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
| `pricing` @ main | ✗ | ✓ | ✓ | ✓ |
| `lru_cache` | ✓ | ✗ | ✗ | ✓ |
| TTL + bound | ✓ | ✓ | ✓ | ✓ |

`demo/target/pricing.py` now caches, so the `untouched` row it used to score is red by construction: the module under test became the thing that passed. That red is the task succeeding.

Same four checks are the task's definition of done:
`make acceptance`

</div>
<div>

**The topologies, asserted** `demo/tests/test_scenarios.py`

```text
solo_strength_zero_coordination_cost
solo_weakness_nobody_checks_the_work
hub_strength_every_hop_touches_the_lead
hub_strength_every_delegation_is_reported_back_and_validated
hub_strength_later_rounds_resume_agents_with_their_context
hub_strength_briefs_are_small
hub_weakness_work_is_sequential
flat_strength_everyone_starts_at_once
flat_strength_finishes_before_hub
flat_weakness_peers_talk_past_the_lead
flat_weakness_more_hops_and_more_context_than_hub
flat_weakness_coder_ships_before_researcher_answers
edges_grow_solo_to_hub_to_flat
```

Run against real logs when present. A red test is a finding.

</div>
</div>

---

# Honest scorecard

| | Solo (control) | Hub (reviewed pipeline) | Flat |
| --- | --- | --- | --- |
| **Agents at once** | 1 | **1** | 3 |
| Wall time | **fastest** here | slower, sequential | fast, parallel |
| Hops | 0 | **fewer**, O(n) | more, O(n²) |
| Rework | one agent's first instinct | **less**: Archie first | more: Codie first |
| Violations at ship | one reflex, unchecked | **0** | lru_cache shipped |
| Context | one window, all of it | small, briefed | large, all read all |

**The hub never had two agents at once, and every run has exactly one writer.** It reviews and contains errors; it does not coordinate. Call it a reviewed pipeline — step 6 is what would change that.

Flat is no strawman: it wins on latency, loses on churn. Nor is solo.

<!--
Speaker: say this out loud. If you make flat look stupid the audience
stops trusting the rest of the talk.

Say the concurrency row out loud too. A test in the repo asserts the
hub never exceeds one agent at a time, so the deck cannot quietly
claim otherwise. Volunteering the limit buys more credibility than
the claim would have.
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

**That first row is for parallelizable work.** The hub run you just watched parallelizes nothing, so it is not what that number measures. More on this on the scorecard.

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

**This is the demo.** One config line moved the run from 4 edges to 12, and changed the code that shipped. What changed was the *spec Codie received*, not the number of writers — only Codie writes, in every run.

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

<div class="figsplit">
<div class="small">

- **A hub stops politics.** No turf war when nobody can flood the shared branch. That is what managers do for people too: psychological safety, not surveillance.
- **The orchestrator's value is decomposition, validation, and synthesis.** Not watching. Manny has no file tools and works better for it.
- **Keep swarms under five.** Use them for parallelism and isolation, the two things a smarter single model cannot do. Everything else: one agent, smaller task.
- **Catch errors early.** Archie before Codie. Better requirements and designs mean fewer bugs, less miscommunication, less churn downstream. Same as it ever was.
- **Adopt the org chart's shape, not its rationale.** Hierarchy solves human problems agents do not have: span of attention, careers, politics, accountability. The one thing that transfers is span of control as a **context** limit. And the chart evolved to coordinate people who were already diverse — your agents are the opposite.

</div>
<div class="figure">

<svg viewBox="0 0 220 400" width="180" role="img" aria-label="A ceiling-mounted artificial intelligence with a single glowing yellow optic.">
  <title>An orchestrator with nobody above it</title>
  <rect x="66" y="0" width="88" height="14" rx="3" fill="#6f757c"/>
  <rect x="92" y="14" width="36" height="30" rx="6" fill="#b9bec4"/>
  <rect x="84" y="42" width="52" height="13" rx="6" fill="#8f959c"/>
  <rect x="94" y="55" width="32" height="34" rx="6" fill="#c6cbd1"/>
  <rect x="84" y="88" width="52" height="13" rx="6" fill="#8f959c"/>
  <rect x="96" y="101" width="28" height="30" rx="6" fill="#b9bec4"/>
  <path d="M32 196 L2 214 L6 262 L30 244 Z" fill="#c8ccd1" stroke="#a5abb2" stroke-width="2"/>
  <path d="M188 196 L218 214 L214 262 L190 244 Z" fill="#c8ccd1" stroke="#a5abb2" stroke-width="2"/>
  <path d="M30 244 L8 268 L18 300 L38 278 Z" fill="#d6dade" stroke="#a5abb2" stroke-width="2"/>
  <path d="M190 244 L212 268 L202 300 L182 278 Z" fill="#d6dade" stroke="#a5abb2" stroke-width="2"/>
  <path d="M34 190 C34 148 186 148 186 190 C193 234 174 292 146 324 C133 342 87 342 74 324 C46 292 27 234 34 190 Z" fill="#eceef0" stroke="#b4bac1" stroke-width="3"/>
  <path d="M36 200 C72 218 148 218 184 200" fill="none" stroke="#c9ced3" stroke-width="3"/>
  <path d="M44 254 C76 268 144 268 176 254" fill="none" stroke="#c9ced3" stroke-width="3"/>
  <path d="M62 300 C82 312 138 312 158 300" fill="none" stroke="#c9ced3" stroke-width="3"/>
  <circle cx="110" cy="312" r="44" fill="#ffca28" opacity="0.2"/>
  <circle cx="110" cy="312" r="32" fill="#d5d8dc" stroke="#b4bac1" stroke-width="3"/>
  <circle cx="110" cy="312" r="25" fill="#33363b"/>
  <circle cx="110" cy="312" r="16" fill="#ffc107"/>
  <circle cx="110" cy="312" r="6" fill="#fff8e1"/>
</svg>

<div class="cap">An orchestrator with nobody above it.<br>She ran the tests, too.</div>

</div>
</div>

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
- This run: the coder reported a summary line he had not produced. The gate output is not the agent's summary of the gate output.
- Every graph, and every number on "By the numbers", is rendered from a JSONL log by a script in this repo.
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

# Questions, comments, concerns?

<div class="qa">

<svg viewBox="0 0 720 300" width="760" role="img" aria-label="The Weighted Companion Cube beside a black forest cake with a lit candle.">
  <title>Questions, comments, concerns?</title>

  <g>
    <path d="M72 118 L128 78 L288 78 L232 118 Z" fill="#b6bfc9"/>
    <path d="M232 118 L288 78 L288 238 L232 278 Z" fill="#6e7a87"/>
    <rect x="72" y="118" width="160" height="160" fill="#939ea9"/>
    <g transform="matrix(1,0,0.35,-0.25,72,118)">
      <circle cx="80" cy="80" r="52" fill="#a4aeb8" stroke="#7d8994" stroke-width="5"/>
      <circle cx="80" cy="80" r="34" fill="none" stroke="#8b96a1" stroke-width="5"/>
    </g>
    <g fill="#cfd6dd">
      <path d="M72 148 L72 118 L102 118 Z"/><path d="M202 118 L232 118 L232 148 Z"/>
      <path d="M232 248 L232 278 L202 278 Z"/><path d="M102 278 L72 278 L72 248 Z"/>
    </g>
    <circle cx="152" cy="198" r="44" fill="#828e9a" stroke="#626e7b" stroke-width="4"/>
    <path d="M152 220 C 126 196 134 170 152 184 C 170 170 178 196 152 220 Z" fill="#ef5aa0"/>
    <g fill="none" stroke="#5d6874" stroke-width="4">
      <rect x="72" y="118" width="160" height="160"/>
      <path d="M72 118 L128 78 L288 78 L288 238 L232 278"/>
      <path d="M232 118 L288 78"/><path d="M232 118 L232 278"/>
    </g>
  </g>

  <g transform="translate(360,0)">
    <ellipse cx="180" cy="252" rx="152" ry="22" fill="#e8e8ee" stroke="#cdcdd8" stroke-width="2"/>
    <path d="M70 140 L70 236 A110 26 0 0 0 290 236 L290 140 Z" fill="#3b2318"/>
    <g stroke="#2a180f" stroke-width="3" stroke-linecap="round" opacity="0.7">
      <path d="M96 168 L96 222"/><path d="M124 178 L124 236"/><path d="M152 182 L152 242"/>
      <path d="M180 183 L180 244"/><path d="M208 182 L208 242"/><path d="M236 178 L236 236"/>
      <path d="M264 168 L264 222"/>
    </g>
    <path d="M70 140 L70 160 A110 26 0 0 0 290 160 L290 140 Z" fill="#fbf4e6"/>
    <path d="M70 152 q14 20 28 4 q16 26 30 2 q16 24 30 4 q14 26 30 2 q16 24 30 0 q16 24 30 -4 q14 20 28 -8" fill="none" stroke="#fbf4e6" stroke-width="13" stroke-linecap="round"/>
    <ellipse cx="180" cy="140" rx="110" ry="26" fill="#fffaf0"/>
    <ellipse cx="180" cy="140" rx="92" ry="21" fill="none" stroke="#efe2cd" stroke-width="3"/>
    <g fill="#c1272d">
      <circle cx="265" cy="148" r="10"/><circle cx="215" cy="159" r="10"/>
      <circle cx="145" cy="159" r="10"/><circle cx="95" cy="148" r="10"/>
      <circle cx="95" cy="132" r="10"/><circle cx="145" cy="121" r="10"/>
      <circle cx="215" cy="121" r="10"/><circle cx="265" cy="132" r="10"/>
    </g>
    <g fill="#ffffff" opacity="0.55">
      <circle cx="262" cy="144" r="3"/><circle cx="212" cy="155" r="3"/>
      <circle cx="142" cy="155" r="3"/><circle cx="92" cy="144" r="3"/>
      <circle cx="92" cy="128" r="3"/><circle cx="142" cy="117" r="3"/>
      <circle cx="212" cy="117" r="3"/><circle cx="262" cy="128" r="3"/>
    </g>
    <rect x="174" y="76" width="12" height="52" rx="3" fill="#f6f1e4" stroke="#e2d9c4" stroke-width="2"/>
    <path d="M180 116 L180 76" stroke="#e2d9c4" stroke-width="2"/>
    <circle cx="180" cy="62" r="20" fill="#ffb74d" opacity="0.28"/>
    <path d="M180 40 C 192 56 190 70 180 76 C 170 70 168 56 180 40 Z" fill="#f79a1e"/>
    <path d="M180 52 C 186 61 185 69 180 72 C 175 69 174 61 180 52 Z" fill="#ffe17a"/>
  </g>
</svg>

<div class="seed">&ldquo;What do the managers think?&rdquo;</div>
<div class="caption">The cake is a lie. The tests are not.</div>

</div>

<!--
Speaker: open the floor with the seed question, not with silence. "What
do the managers think?" puts the room in the chair the whole talk argued
for, and it works on engineers too: it asks them to judge the work
instead of the tooling.

The two props are the promises Portal makes and breaks: the cube is the
teammate you are issued and then told to incinerate, the cake is the
reward that never arrives. Both are what a multi-agent demo sells. The
answer to "does any of this actually work?" is `make acceptance`, not a
slide. Sources are the next slide if anyone wants a citation.

If asked for the number, this is the gate on the hub branch, verbatim:

  4 passed, 10 deselected in 0.01s
  [1 caches repeats] [2 refreshes after 5s] [3 bounded memory] [4 errors not cached]

Zero skipped, zero xfailed. The ten deselected are the unit tests, which
`-m acceptance` filters out; they pass in their own run.
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
