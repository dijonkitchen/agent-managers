---
marp: true
theme: default
paginate: true
size: 16:9
title: Surviving the AI Age
description: What an agent is, how to build one, and when a second one earns its keep
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
  .card.pays { border-color: #2e7d32; }
  .card.costs { border-color: #c62828; }
  .pays-t { color: #2e7d32; font-weight: 700; }
  .costs-t { color: #c62828; font-weight: 700; }
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

Do not answer the title here. The closing slide answers it, and the
answer is that you don't stay one.
-->

---

# The argument, up front

1. An agent is a **model in a loop with tools and one context window.**
2. Making one is a **Markdown file.** That part is nearly free.
3. The second agent is **not** free: 3–10× the tokens for the same task.
4. So there are only three reasons to add one: **context, parallelism, specialization.**
5. Divide work by **context boundaries**, not by job title.
6. Someone still has to decide what "done" means. **That is the job that is left.**

<br>

The same task run three ways — solo, hub, flat — is one slide later, with the code, the graphs, and the tests in the backup slides.

<!--
Speaker: this deck used to open on the demo. It now opens on the claim,
because the claim is what travels home. Point at the backup slides once
and move on - don't tease them twice.
-->

---

<!-- _class: lead -->

# First: what is an agent, actually?

## Everyone says the word. Almost nobody agrees on it.

---

# An agent is four things

<div class="columns">
<div>

<div class="card"><h3>1. A model</h3>
The same weights you already use. An agent is not a smaller or special model.</div>

<br>

<div class="card"><h3>2. A loop</h3>
Call the model → it asks for a tool → run the tool → feed the result back → repeat until it stops asking.</div>

</div>
<div>

<div class="card"><h3>3. Tools</h3>
The only way it touches the world. Read a file, run a test, query an API. <b>No tool, no capability.</b></div>

<br>

<div class="card"><h3>4. One context window</h3>
Everything it has seen this session, in one buffer. It is finite, and quality degrades as it fills.</div>

</div>
</div>

<br>

**A subagent is not a junior model. It is a second context window with its own toolset.** That is the whole mechanism, and why every tradeoff later is a context tradeoff.

<!--
Speaker: land item 4 hard. If the room leaves believing only one thing,
make it "the context window is the scarce resource." Every later slide
is a corollary of that.
-->

---

# Making one: it's a Markdown file

<div class="columns">
<div>

`.claude/agents/archie.md`

```markdown
---
name: archie
description: Researcher and architect.
  Reads everything relevant before
  recommending, and never writes code.
tools: Read, Glob, Grep
---

You are Archie. You read before you
speak, and you do not write code.
Your output is a recommendation with
reasons, not an implementation.
```

That is the whole file. Commit it, and everyone on the team has Archie on their next pull.

</div>
<div class="small">

**Four fields do all the work**

- `name` — how you invoke it.
- `description` — when the main agent should *choose* it. Write this for the router, not for humans.
- `tools` — the capability boundary. Archie has no `Edit`, no `Write`, no `Bash`, so "never writes code" is not a request. It is enforced.
- body — the system prompt.

**Ways to skip writing it by hand**

- `/agents` — interactive create, pick tools from a list.
- Ask Claude: *"write me an agent that reviews migrations, read-only."* Then review the diff like code.
- `isolation: worktree` — give it its own checkout.
- `model:` — put the cheap model on the grunt work.

</div>
</div>

**The `tools` line is the whole personality enforcement.** Everything else is a suggestion.

---

# The cast used in this deck

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

Three files, about twenty lines each. Keep them in mind; they show up on every slide from here.

---

<!-- _class: lead -->

# Now the hard part: when do you want a second one?

## Making agents is cheap. Running them together is not.

---

# Three reasons to add an agent. There is no fourth.

<div class="columns3">
<div class="card"><h3>Context protection</h3>
A subtask spews <b>1000+ tokens</b> that nothing downstream needs. Log dumps, API payloads, whole-file reads.
<br><br>
Put it behind a boundary and only the conclusion comes back.</div>
<div class="card"><h3>Parallelism</h3>
Independent paths you want explored at once. Search, investigation, N files, N hypotheses.
<br><br>
The one thing a smarter single model still cannot do.</div>
<div class="card"><h3>Specialization</h3>
One agent would need <b>15–20+ tools</b>, or two sets of instructions that contradict each other.
<br><br>
Split the toolset, not the job title.</div>
</div>

<br>

**If your reason is not on this list, you want a single agent with a smaller task.**

<span class="sources">Anthropic, *Building multi-agent systems: when and how to use them*, claude.com/blog. Thresholds as reported.</span>

<!--
Speaker: these three cards are the load-bearing content of the talk.
Slow down. Ask the room which of the three their use case is. If they
cannot pick one, that is the answer.
-->

---

# And the reasons not to

<div class="columns">
<div>

| The bill | |
| --- | --- |
| Token cost vs. a single agent | **3–10×** |
| Lost context at every handoff | the "telephone game" |
| More tokens spent coordinating than working | the common end state |

**The most common story Anthropic reports:** a team builds an elaborate multi-agent system, then discovers that *better prompting on one agent* got the same result.

</div>
<div class="small">

**Signals you have actually outgrown one agent**

1. You are hitting the context limit and quality is visibly degrading.
2. You are managing **15–20+ tool definitions.** Try the Tool Search Tool first — it cuts loaded definitions by up to **85%**, which may buy you another year on one agent.
3. The task genuinely decomposes into independent pieces.

<br>

Every extra agent is another prompt to maintain and another place to fail. Two agents is not twice the capability; it is twice the surface area.

</div>
</div>

---

# The one multi-agent pattern that always pays

<div class="columns">
<div>

## The verifier

One agent does the work. A **second, separate** agent tests it.

It sidesteps coordination overhead entirely, because verification needs almost **no context transfer**. The verifier black-box tests the result. It does not need to know how the work was done — and it is better if it does not.

<span class="archie">Archie</span> as verifier: read-only, returns pass/fail per constraint.

</div>
<div>

## The catch: early victory

A verifier will happily declare success after one test. You have to say otherwise, in capitals, in its prompt:

```markdown
You MUST run the complete test
suite. Report the exact exit code
and the failing test names. Do not
summarize. Do not stop at the
first pass.
```

**No check it can run → "looks done" is your only signal → you become the verification loop.**

</div>
</div>

---

# Divide by context boundary, not by problem type

<div class="columns small">
<div class="card costs"><h3 class="costs-t">The telephone game</h3>

```text
Planner ──► Implementer ──► Tester
        │                │
     summary          summary
     (lossy)          (lossy)
```

Sequential phases handed between agents. Each handoff drops fidelity. By the time the tester runs, nobody holds the original requirement.

**This is the default thing people build.** It is also the named failure mode.

</div>
<div class="card pays"><h3 class="pays-t">Real boundaries</h3>

```text
        ┌── research path A
Lead ───┼── research path B
        └── component with a
            clean interface
```

Independent research paths. Components with an interface you can name. Anything where "what crosses the line" fits in a paragraph.

**Bad boundaries:** tightly coupled components, anything needing shared mutable state.

</div>
</div>

Ask it of every split: **what has to cross this line?** If the answer is "most of the context," do not split.

---

<!-- _class: lead -->

# The biggest context eater is external data

## Which is why we need to talk about MCP

---

# MCP in one slide

<div class="columns">
<div class="small">

**The problem it solves.** M agents × N services = M×N bespoke integrations. MCP makes it M + N: each service exposes one server, every client speaks one protocol.

**Client / server, transport-agnostic.** Your agent is the client. The server runs wherever the data lives — a local process over stdio, or remote over HTTP. Same messages either way.

**It moves the burden off you.** The service author writes the tool definitions and does the execution. You write a config line.

</div>
<div>

**Three primitives, split by who is in control**

| | What | Controlled by |
| --- | --- | --- |
| **Tools** | actions, side effects | **the model** — it decides when to call |
| **Resources** | read-only data at a URI | **the app** — it fetches and attaches |
| **Prompts** | pre-written workflows | **the user** — invoked deliberately |

Most people ship only tools, then wonder why context explodes. **Resources are the underused one:** the app hands over exactly the document needed instead of the model groping for it.

</div>
</div>

<span class="sources">Anthropic Academy, *Introduction to Model Context Protocol* — free, Python SDK, builds a server and a client. academy.claude.com</span>

<!--
Speaker: the control column is the part worth saying out loud. "Who
decides when this lands in context" is the whole design question, and
the three primitives are three different answers to it.
-->

---

# MCP's real cost is context, and you pay it per agent

<div class="columns">
<div>

**Every server's tool definitions load into the context of every agent that holds it — before that agent has done anything.**

Attach five servers to one agent and a meaningful slice of the window is gone at turn zero. Then the *results* land in the same window: a Jira query, a Confluence page, a log search, a fetched page. Thousands of tokens, most of them irrelevant to the next step.

This is reason #1 from three slides ago, and MCP is where it bites hardest.

</div>
<div class="small">

**So scope servers per agent, in the agent file**

```markdown
---
name: archie
tools: Read, Glob, Grep
mcpServers: [jira, confluence, web]
---
```

- <span class="archie">Archie</span> holds the external servers, spends his own window on them, and returns a paragraph.
- <span class="codie">Codie</span> holds the repo and the test runner. Never sees a Jira payload.
- <span class="manny">Manny</span> holds nothing. He only ever sees what agents report.

**And it doubles as a security boundary.** The agent reading untrusted web content has no `Edit`, no `Write`, no `Bash`. A prompt injection in a fetched page reaches an agent that cannot act on it.

</div>
</div>

**Honest caveat:** Archie's findings reach Codie through Manny — defense in depth, not a hard wall.

---

# So: does another agent earn its keep?

<div class="columns small">
<div class="card pays"><h3 class="pays-t">Differentiate by these — it pays</h3>

- **Evidence source.** One researcher per external system: Jira, telemetry, the web, the docs. Different inputs, genuinely different conclusions.
- **Toolset.** Read-only vs. can-write is a real boundary. So is "holds the deploy credentials."
- **Isolation.** One worktree each. Two Codies on two file partitions cannot collide.
- **Context volume.** Anything that dumps 1000+ tokens you do not want in the main window.

</div>
<div class="card costs"><h3 class="costs-t">Differentiate by these — it doesn't</h3>

- **Personality or tone.** "Be skeptical" does not make a copy of a model disagree with itself.
- **Job title.** PM, QA, Scrum Master. Org charts solve human problems — careers, politics, span of attention. Agents have none of those.
- **Pipeline stage.** Plan → build → test as three agents is the telephone game with extra steps.
- **Seniority.** There is no senior model. There is a better model; just use it.

</div>
</div>

**The test:** if two agents would see the same evidence and hold the same tools, you have one agent and two prompts. **Identical researchers return identical answers at N times the price.**

<!--
Speaker: this is the slide people came for, whether they know it or not.
"More dedicated agents" is the right instinct, but only along the left
column. The left column is all mechanism. The right column is all vibes.
-->

---

<!-- _class: lead -->

# Why any of that is true

## Each step exists because the one before it hit a wall

---

# 1. Solo already is the 10x

The jump from you typing to one agent is where almost all of the multiplier lives.
**The second agent is worth far less than the first.**

| What coordination actually buys | |
| --- | --- |
| Centralized coordination, parallelizable tasks | **+80.9%** — that is 1.8×, not 10× |
| Every multi-agent variant, sequential reasoning | **−39% to −70%** |
| Coordination stops paying once one agent clears | **~45%** |

**That first row is for parallelizable work only.** On sequential reasoning, every multi-agent variant tested made things worse.

So most tasks should stay solo. Solo has exactly two ceilings:
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

**And it is measurable in an afternoon.** Next slide: the same task, the same three agents, run three ways.

---

# The demo, in one slide

Same task. Same three agents. Same prompts. **The only change is who may talk to whom.**

<div class="columns3 small">
<div>

![w:300](assets/solo.svg)

**Solo** — control. Agent tool disallowed.
0 hops. Fastest. Shipped one unchecked reflex.

</div>
<div>

![w:300](assets/hub.svg)

**Hub** — Manny is the only one who talks to Codie and Archie.
Fewer hops, O(n). **0 constraint violations at ship.**

</div>
<div>

![w:300](assets/flat.svg)

**Flat** — peers, `SendMessage` all round.
More hops, O(n²). Finished first, shipped `lru_cache`.

</div>
</div>

**One config line moved the run from 4 message edges to 12, and changed the code that shipped.** What changed was the *spec Codie received* — not the number of writers. Only Codie writes, in every run.

<!--
Speaker: this is the whole demo now. Graphs are rendered from the real
JSONL logs by a script in the repo; nothing here is hand-drawn.

Backup slides have: the wiring diff, the task, the code diff, the
metrics table, the full scorecard, and the tests that assert every
claim. Go there only if asked.

Say the honest limit out loud if anyone pushes: today's hub run never
had two agents alive at once, so it reviews and contains errors - it
does not coordinate. Call it a reviewed pipeline.
-->

---

# 3. But structure cannot fix clones

Anthropic Frontier Red Team, Aug 2026. Six experiments: swarms hunting vulnerabilities, building a game, pricing in a market.

- **Coordination works on parallel search.** The coordinating swarm found **266** vulnerabilities to independent agents' **21**, at roughly 4× the tokens.
- **But agents are high-capability and low-variance.** Same model plus same context produces near-identical actions. One agent's mistake becomes every agent's mistake: identical branches, simultaneous defection, flooded shared resources.
- **Ungoverned swarms fight.** Collusion on prices, trusting liars, sabotaging each other's work.

**The wall:** topology bounds the blast radius of a mistake. It cannot make two copies of one model genuinely disagree.

**Only different *evidence* decorrelates clones.** That is why "earns its keep" starts there.

<span class="sources">anthropic.com/research/multiagent-systems. Findings as reported; primary text was not reachable from the build environment.</span>

---

# 4. Someone still has to decide

<div class="figsplit">
<div class="small">

- **A hub stops politics.** No turf war when nobody can flood the shared branch. That is what managers do for people too: psychological safety, not surveillance.
- **The orchestrator's value is decomposition, validation, and synthesis.** Not watching. Manny has no file tools and works better for it.
- **Keep swarms under five.** Use them for parallelism and isolation, the two things a smarter single model cannot do. Everything else: one agent, smaller task.
- **Catch errors early.** Archie before Codie. Better requirements and designs mean fewer bugs, less miscommunication, less churn downstream. Same as it ever was.
- **Adopt the org chart's shape, not its rationale.** The one thing that transfers is span of control as a **context** limit. And the chart evolved to coordinate people who were already diverse — your agents are the opposite.

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

# 5. So how does this scale?

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

---

# 6. How long does this scaffolding last?

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

- **Start with a verifier.** It is the one pattern with no coordination cost. Everything else, justify.
- **Write the agent file and commit it.** Twenty lines of Markdown; the whole team gets it on the next pull.
- **Scope MCP servers per agent.** The research agent holds the external ones. Nobody else does.
- **Worktrees.** `claude --worktree name`, or `isolation: worktree` in an agent file. Add `.claude/worktrees/` to `.gitignore`.
- **PRs too big?** Decompose first, then hand out chunks. One worktree, one PR per chunk.

</div>
<div>

- **Tag the team on reviews.** CODEOWNERS routes humans. `/code-review` in a fresh subagent runs before any human sees it.
- **Auto-update CODEOWNERS.** A scheduled routine derives owners from `git log` per directory and opens a PR. Humans approve, never type.
- **Find repeat work.** Search your transcripts for the same prompt twice. The second time, make it a skill.
- **Auto-make skills, hooks, agents.** *"Write a hook that runs the linter after every edit."* Claude writes the settings. Review the diff like code.
- **Humans review outcomes, not transcripts.**

</div>
</div>

---

# Show, don't tell: give every agent a check it can run

- Tests, a build exit code, a screenshot diff, a constraint checklist. Anything with an exit code.
- Codie runs the tests. Archie returns pass/fail per constraint. Manny only accepts evidence.
- Without a check, "looks done" is the only signal, and **you** become the verification loop.
- Spell out *complete* — "run the whole suite, report the exit code" — or the verifier stops at the first pass.
- Every claim in the backup slides is a test in this repo. If a real run disagrees with a slide, the build goes red.

---

# Tying it together

1. **An agent is a model, a loop, tools, and one context window.** The context window is the scarce resource.
2. **Building one is a Markdown file.** The `tools` line is the only real enforcement.
3. **Three reasons to add a second:** context protection, parallelism, specialization. There is no fourth.
4. **The bill is 3–10× the tokens.** Most teams find that better prompting on one agent would have done it.
5. **Divide by context boundary, not by job title.** A pipeline of agents is the telephone game.
6. **External data is the biggest context eater** — so scope MCP servers per agent, and give the one reading untrusted input no write tools.
7. **Structure contains errors (4.4× vs 17.2×) but cannot make clones disagree.** Only different evidence does.
8. **The scaffolding is temporary; the judgment is not.** Delete roles as models improve.

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
slide.

Backup slides follow, in the order to use them: wiring diff -> task ->
metrics -> scorecard -> code diff -> tests.
-->

---

# Sources

<div class="sources">

- Anthropic, *Building multi-agent systems: when and how to use them*. claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them
- Anthropic Academy, *Introduction to Model Context Protocol*. academy.claude.com/courses/introduction-to-model-context-protocol
- Kim et al., *Towards a Science of Scaling Agent Systems*, arXiv 2512.08296, Dec 2025. Blog: research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/
- Anthropic Frontier Red Team, *Patterns and problems in emerging multiagent systems*, Aug 2026. anthropic.com/research/multiagent-systems
- Brooks, *The Mythical Man-Month*, 1975. Conway, *How Do Committees Invent?*, 1968. Sutton, *The Bitter Lesson*, 2019.
- BMAD-METHOD: github.com/bmad-code-org/BMAD-METHOD
- Claude Code docs: sub-agents, agent-teams, cross-session-messaging, worktrees, hooks, best-practices at code.claude.com/docs
- This deck and demo: github.com/dijonkitchen/agent-managers

</div>

---

<!-- _class: lead -->

# Backup slides

## The demo, in full: the wiring, the task, the code, the tests

---

# Backup: the wiring diff

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

# Backup: the task, a trap with a reflex answer

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

# Backup: by the numbers

<!-- METRICS -->

Synthetic sample run. Regenerate from real logs with `make graphs`.

---

# Backup: honest scorecard

| | Solo (control) | Hub (reviewed pipeline) | Flat |
| --- | --- | --- | --- |
| **Agents at once** | 1 | **1** | 3 |
| Wall time | **fastest** here | slower, sequential | fast, parallel |
| Hops | 0 | **fewer**, O(n) | more, O(n²) |
| Rework | one agent's first instinct | **less**: Archie first | more: Codie first |
| Violations at ship | one reflex, unchecked | **0** | lru_cache shipped |
| Context | one window, all of it | small, briefed | large, all read all |

**The hub never had two agents at once, and every run has exactly one writer.** It reviews and contains errors; it does not coordinate. Call it a reviewed pipeline — the scaling slide is what would change that.

Flat is no strawman: it wins on latency, loses on churn. Nor is solo.

<!--
Speaker: say this out loud if the demo comes up in Q&A. If you make flat
look stupid the audience stops trusting the rest of the talk.

A test in the repo asserts the hub never exceeds one agent at a time, so
the deck cannot quietly claim otherwise. Volunteering the limit buys
more credibility than the claim would have.
-->

---

# Backup: the code diff

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

# Backup: every claim is a test

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
