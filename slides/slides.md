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
  .columns > *, .columns3 > *, .figsplit > * { min-width: 0; }
  /* Fixed layout keeps a wide table inside its grid column; the label column
     gets enough of it that short headers do not break mid-word. */
  .columns table, .columns3 table { table-layout: fixed; width: 100%; }
  .columns th:first-child, .columns td:first-child { width: 30%; }
  .columns td, .columns3 td { overflow-wrap: break-word; }
  .small { font-size: 21px; }
  /* Name colours are also used as small body text, so they are darkened to
     clear 4.5:1 on white rather than matching the agent swatches exactly. */
  .codie { color: #c1481c; } .archie { color: #2f6ac0; } .manny { color: #8a6600; }
  .card { border: 2px solid #ddd; border-radius: 10px; padding: 0.6rem 0.9rem; }
  .card h3 { margin: 0 0 0.3rem 0; }
  .sources { font-size: 18px; }
  .scratched { font-size: 38px; font-weight: 700; color: #b0b0b0;
    text-decoration: line-through; text-decoration-color: #d64545;
    text-decoration-thickness: 4px; line-height: 1.3; }
  .byline { margin-top: 1.8rem; font-size: 24px; color: #555; }
  .chili { vertical-align: -7px; margin-right: 0.3rem; }
  section.lead h1 .title { font-size: 52px; line-height: 1.15; }
  .figsplit { display: grid; grid-template-columns: 2.5fr 1fr; gap: 1.2rem; align-items: center; }
  .figure { text-align: center; }
  .figure .cap { font-size: 18px; color: #5a5a5a; line-height: 1.35; }
  .qa { text-align: center; }
  .qa svg { display: block; margin: 0 auto 0.4rem; }
  .qa .seed { font-size: 28px; font-weight: 700; color: #2d3b4e; line-height: 1.35; }
  .qa .caption { font-size: 22px; color: #666; margin-top: 0.2rem; }
  pre { font-size: 18px; }
  table { font-size: 21px; }
  /* Ten metric rows plus the generated provenance caption, which the deck
     must show in full: it is the only claim it makes about where the
     numbers came from. */
  section.metrics table { font-size: 20px; }
  section.metrics p { font-size: 17px; color: #555; }
  /* The ladder climbs: rung 0 sits bottom-left, rung 10 top-right, so the
     rows are authored top-down from 10 and each one is indented less than
     the row above it. */
  .stair { margin-top: 0.3rem; }
  .stair .step { font-size: 18px; line-height: 1.25; padding: 3px 12px;
    margin-bottom: 4px; border-left: 5px solid #cfd6dd; background: #f6f7f9;
    display: table; border-radius: 0 4px 4px 0; }
  .stair .step b { color: #2d3b4e; margin-right: 0.45rem; }
  .stair .top { border-left-color: #2d3b4e; background: #eef1f5; }
  .stair .wall { font-weight: 400; }
  .stair .i0  { margin-left: 0; }      .stair .i1  { margin-left: 42px; }
  .stair .i2  { margin-left: 84px; }   .stair .i3  { margin-left: 126px; }
  .stair .i4  { margin-left: 168px; }  .stair .i5  { margin-left: 210px; }
  .stair .i6  { margin-left: 252px; }  .stair .i7  { margin-left: 294px; }
  .stair .i8  { margin-left: 336px; }  .stair .i9  { margin-left: 378px; }
  .stair .i10 { margin-left: 420px; }
  .wall { color: #b03030; font-weight: 700; }
  .rung { font-weight: 700; color: #2d3b4e; }
  .tenx { font-size: 30px; font-weight: 700; color: #2d3b4e; }
  blockquote { border-left: 5px solid #ddd; margin-left: 0; padding-left: 1rem;
    font-size: 30px; color: #333; }
  blockquote footer { font-size: 20px; color: #666; }
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

The deck is a ladder. Every rung is the same two moves: you get faster,
then you hit a wall that the next rung exists to clear. Ask "how do we
10x again?" out loud at each wall -- the room will start answering
before you do, and the last answer is the thesis.

Do not answer the title here. The closing slide answers it, and the
answer is that you don't stay one.
-->

---

# The ladder

<div class="stair">
<div class="step i10 top"><b>10</b> <b>Manage</b> — that one is yours</div>
<div class="step i9"><b>9</b> Delete orchestration the models outgrow <span class="wall">→ nothing left to automate but judgment</span></div>
<div class="step i8"><b>8</b> Buy the cast (BMAD); fan out (<code>/batch</code>) <span class="wall">→ the scaffolding rots</span></div>
<div class="step i7"><b>7</b> Diversify by evidence: MCP, context, skills <span class="wall">→ you are hand-rolling an org chart</span></div>
<div class="step i6"><b>6</b> Wire the fleet deliberately <span class="wall">→ clones, cost, agents that fight</span></div>
<div class="step i5"><b>5</b> Delegate: each session gets its own agents <span class="wall">→ a fleet with no structure</span></div>
<div class="step i4"><b>4</b> You become the hub <span class="wall">→ you are the bottleneck, and tired</span></div>
<div class="step i3"><b>3</b> Isolate them: worktrees, <code>claude -w</code> <span class="wall">→ N tabs, all asking you</span></div>
<div class="step i2"><b>2</b> Several agents in one repo <span class="wall">→ they overwrite each other</span></div>
<div class="step i1"><b>1</b> One agent: hooks, skills, delegation <span class="wall">→ it cannot be in two places</span></div>
<div class="step i0"><b>0</b> Type code yourself <span class="wall">→ one head, one file at a time</span></div>
</div>

Start at the bottom. Each rung buys speed, then hands you the wall that sends you up.
**The talk is mostly about when to stop climbing.**

---

# Rung 1: three primitives, three different jobs

<div class="columns3">
<div class="card"><h3>Hooks</h3>
<b>Deterministic actions.</b><br>
Shell commands the harness runs on an event — not something the model decides.<br>
<span class="small">Format after every edit. Block a commit to <code>main</code>. Log every spawn.</span></div>
<div class="card"><h3>Skills</h3>
<b>Differentiated workflows.</b><br>
A named procedure, loaded only when it is relevant.<br>
<span class="small">The second time you type the same prompt, it should have been a skill.</span></div>
<div class="card"><h3>Agents</h3>
<b>Parallelism and isolation.</b><br>
A separate context with its own tools.<br>
<span class="small">Fan out over files, sources, hypotheses. The only primitive that costs real tokens.</span></div>
</div>

**Reach in that order.** If a hook can do it, a skill should not. If a skill can do it, an agent should not.

<!--
Speaker: this slide exists so nobody spends the talk thinking every
problem needs a swarm. Most repos get more from four hooks and two
skills than from any topology on this deck.
-->

---

# Rung 2: you can manage one. Now manage more.

One agent is a conversation: you ask, it works, you read the diff, you ask again.

**The obvious scale-up is the org chart's oldest move — hire.** Run three.

<div class="columns">
<div>

```sh
# three terminals, one repo
claude "add the cache"
claude "port the tests to pytest"
claude "update the docs"
```

</div>
<div>

**What you expect:** three times the throughput.

**What you get:** the next slide.

</div>
</div>

---

# Rung 2 breaks: three agents in one repo fight

<div class="columns">
<div class="small">

- Two edit `pricing.py` in the same minute. The second read a stale file.
- One runs the suite mid-write by another. The red is a race, not a bug.
- All three commit to one branch. Nothing can be reverted alone.
- Your tree is a merge of three plans, and **you** tell them apart.

</div>
<div>

**This is thrash, and it is not an agent problem.** Put three humans on one checkout with no branches and you get the same afternoon.

The fix is the same one we already use for people, and for the same reason:

<span class="tenx">Give each worker its own copy.</span>

</div>
</div>

---

# Rung 3: isolate the work

<div class="columns small">
<div>

**By checkout.** One git worktree each: own directory, own branch, shared object store. Nobody sees a half-written file.

**By partition.** Sharing a tree? Each agent owns a directory; the others may not write there.

**By context.** Separate sessions do not share history. The docs agent never sees the cache debate.

</div>
<div>

**What isolation buys**

- Races become impossible, not unlikely.
- One branch, one PR per chunk, reviewable alone.
- A failed run is deleted, not untangled.
- **The one thing a smarter model cannot do for you:** no model is in two worktrees at once.

**The cost:** merges. The conflict moves from your tree to review time.

</div>
</div>

---

# `claude -w`, in one slide

```sh
claude -w                      # new worktree + branch for this session
claude -w cache-ttl            # ... with a name you choose
claude -w cache-ttl --tmux     # ... and a tmux window/pane to watch it in
```

<div class="columns small">
<div>

Same thing inside an agent definition, so a spawn gets its own tree:

```yaml
---
name: codie
tools: Read, Edit, Write, Bash
isolation: worktree
---
```

And the housekeeping:

```sh
claude agents          # every background session, one view
claude rm <id>         # delete a session and its worktree
```

</div>
<div>

**House rules**

- Add the worktree directory to `.gitignore` — this repo uses `.worktrees/`, one per run, named `<run>-<timestamp>`.
- Start every worktree from the same commit, or you are comparing different codebases.
- The worktree is disposable; **the branch is the output**. `make clean-worktrees` drops the trees and keeps the branches.

`demo/lib/worktree.sh` is 30 lines and does exactly this.

</div>
</div>

---

# So you are a 10x engineer now, right?

<div class="columns">
<div>

```text
tab 1  codie      cache-ttl      ● waiting on you
tab 2  codie      pytest-port    ● waiting on you
tab 3  archie     rate-limits    ○ working
tab 4  claude     docs           ● waiting on you
tab 5  claude     flaky-test     ● waiting on you
```

Five isolated sessions. No races. Every one of them **stopped to ask you something**.

</div>
<div>

**The arithmetic that does not work**

One session asks you roughly one question every few minutes.

Five sessions ask five. Ten ask ten.

Throughput is no longer bounded by the agents. It is bounded by **how fast you can be interrupted**.

</div>
</div>

---

# Rung 3 breaks: the wheel

<div class="figsplit">
<div class="small">

- Every answer needs the context that session was in. Five sessions are five contexts, and none of them is the one you were just in.
- A context switch costs you minutes on each side of it — and the agent was idle for all of them.
- The questions are cheap individually and ruinous in aggregate: *"which branch?", "is this test meant to be skipped?", "can I install this?"*
- You stop doing engineering. You become the runtime: a scheduler with a human latency of thirty seconds.
- **And it is draining in a way raw work is not.** You end the day having typed nothing and having decided everything.

**Running faster inside the wheel is not the fix.**

</div>
<div class="figure">

<svg viewBox="0 0 260 250" width="250" role="img" aria-label="A rat running inside a wheel that is going nowhere.">
  <title>Effort without travel</title>
  <path d="M40 232 L70 176 M220 232 L190 176" stroke="#8f959c" stroke-width="7" stroke-linecap="round"/>
  <rect x="24" y="228" width="212" height="10" rx="5" fill="#8f959c"/>
  <circle cx="130" cy="120" r="92" fill="none" stroke="#b4bac1" stroke-width="7"/>
  <circle cx="130" cy="120" r="80" fill="none" stroke="#c9ced3" stroke-width="4"/>
  <g stroke="#ccd1d6" stroke-width="4">
    <path d="M130 40 L130 200"/><path d="M50 120 L210 120"/>
    <path d="M73 63 L187 177"/><path d="M187 63 L73 177"/>
    <path d="M92 47 L168 193"/><path d="M168 47 L92 193"/>
    <path d="M57 82 L203 158"/><path d="M203 82 L57 158"/>
  </g>
  <circle cx="130" cy="120" r="12" fill="#b4bac1"/>
  <g>
    <path d="M96 176 C 96 150 118 140 140 142 C 168 144 182 160 180 176 Z" fill="#9aa0a8"/>
    <path d="M178 150 C 192 146 200 154 198 164 C 196 174 186 178 180 176 Z" fill="#a8aeb6"/>
    <circle cx="176" cy="147" r="10" fill="#c3a3ad"/>
    <circle cx="176" cy="147" r="5" fill="#d8bcc4"/>
    <circle cx="192" cy="158" r="3.2" fill="#2f3338"/>
    <circle cx="199" cy="166" r="2.4" fill="#5a6068"/>
    <path d="M96 168 C 72 168 62 152 54 140" fill="none" stroke="#b6a0a6" stroke-width="5" stroke-linecap="round"/>
    <path d="M118 176 L112 194 M146 176 L152 194 M132 176 L130 196" stroke="#9aa0a8" stroke-width="6" stroke-linecap="round"/>
  </g>
  <g fill="none" stroke="#7d8994" stroke-width="4" stroke-linecap="round" opacity="0.65">
    <path d="M214 74 A 96 96 0 0 1 226 110"/>
    <path d="M196 50 A 96 96 0 0 1 210 66"/>
  </g>
  <path d="M232 104 L240 118 L224 118 Z" fill="#7d8994" opacity="0.65"/>
</svg>

<div class="cap">Five sessions, zero context switches<br>that were free.</div>

</div>
</div>

---

# Rung 4: the first structure — and you are the hub

<div class="columns">
<div>

```text
        you
    ┌────┼────┬────────┐
  sess1 sess2 sess3  sess4
```

Every question, every decision, every "is this in scope" goes through one node, and the node is you.

**Good news:** this is a real topology, and it is the one with the best error containment. Nothing reaches the shared branch without passing a reviewer.

</div>
<div class="small">

**Why it feels bad anyway**

- **n&minus;1 links**, all attached to one person.
- Your context window is the smallest in the system — and the only one that cannot be extended.
- Every session idles while you are in another. Isolation fixed thrash, not latency.
- You are doing decomposition, routing, validation and synthesis. **Four jobs.**

The shape is right. Being personally at the center of it is what does not scale.

</div>
</div>

---

<!-- _class: lead -->

# How do you 10x from here?

## <span class="tenx">Delegation.</span> Stop being the hub. Hire one.

---

# Rung 5: give each session its own agents

<div class="columns">
<div>

**Before** — you answer every question

```text
you ──► session ──► (question) ──► you
```

**After** — the session answers most of them

```text
you ──► lead ──┬──► researcher
               ├──► coder
               └──► reviewer
```

You answer what only you can: scope, tradeoffs, "ship it".

</div>
<div class="small">

**What actually changed**

- The lead takes decomposition, routing and first-pass validation — **the three jobs that were never judgment.**
- Questions the repo can answer get answered in the repo, not by you.
- You are still interrupted, but **per session, not per agent** — and pre-summarized.

**The rule:** a delegate that cannot check its own work sends the check back to you. Give every agent something it can run.

</div>
</div>

---

# Making an agent, and wiring who talks to whom

<div class="columns small">
<div>

**An agent is a Markdown file.**

```yaml
---
name: archie
description: Researcher and architect. Reads
  everything before recommending. Never
  writes code.
tools: Read, Glob, Grep      # the enforcement
model: opus
isolation: worktree
---
You read before you speak. Report pass or
fail per constraint, with the test that
proves it.
```

`description` decides *when* it is picked. `tools` is the whole personality enforcement: Archie cannot write code because he has no `Edit`.

</div>
<div>

**Wiring is a separate decision from staffing.**

| | Who can talk |
| --- | --- |
| **Subagents** | child → parent only. No `SendMessage`, so no side channels. |
| **Agent teams** | every teammate gets `SendMessage`. Anyone → anyone. |
| **Named + resumed** | `Agent(name: "codie")`, then `SendMessage("codie", …)` — same agent, keeps its context. |
| **Cross-session** | your own sessions message each other by name. |

**Resuming beats re-briefing.** A fresh agent needs the whole story; a named one needs only what changed. The hub run's biggest hop was a cold brief: 17.4k chars.

</div>
</div>

---

# The cast: three agents, in this repo

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

Definitions are plain Markdown in `.claude/agents/`. Nothing here is a framework: three files, one hook, three shell scripts.

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

**Three env vars and a flag.** That is the entire difference between the runs you are about to see.

---

# Now each session does more

<div class="columns">
<div>

```text
you
├── lead A ──┬── archie
│            └── codie × 2   (2 worktrees)
├── lead B ──┬── archie
│            └── codie
└── lead C ─── codie
```

Same five interruptions an hour. Roughly three times the work underneath them.

</div>
<div class="small">

**What you should notice**

- You did not get faster at answering. The unit of work behind each answer got bigger.
- Every leaf is isolated, so the `codie × 2` is genuine parallelism and not a race.
- The leads are where context lives. Yours stays empty on purpose — that is the point of Manny having no file tools.

**And the obvious next thought is the dangerous one:** if two leads are good, are ten better?

</div>
</div>

---

<!-- _class: lead -->

# How do you 10x again?

<div class="qa">

<svg viewBox="0 0 720 320" width="720" role="img" aria-label="A dense industrial town of workshops, pipes, gears and smoking chimneys, with one small figure at the gate.">
  <title>Industrialize it</title>
  <rect x="0" y="0" width="720" height="320" fill="#f4f2ee"/>
  <g fill="#e6e2db">
    <circle cx="150" cy="60" r="34"/><circle cx="188" cy="48" r="26"/><circle cx="118" cy="52" r="22"/>
    <circle cx="470" cy="44" r="30"/><circle cx="508" cy="56" r="22"/><circle cx="436" cy="58" r="20"/>
    <circle cx="300" cy="34" r="22"/><circle cx="330" cy="46" r="16"/>
  </g>
  <g fill="#c7cbd0" stroke="#aeb4bb" stroke-width="2">
    <rect x="28" y="150" width="90" height="118"/>
    <rect x="600" y="140" width="96" height="128"/>
    <rect x="250" y="120" width="70" height="148"/>
  </g>
  <g fill="#b0b6bd" stroke="#969ca4" stroke-width="2">
    <rect x="126" y="176" width="112" height="92"/>
    <rect x="330" y="164" width="120" height="104"/>
    <rect x="462" y="186" width="128" height="82"/>
  </g>
  <g fill="#9aa1a9">
    <path d="M126 176 L182 140 L238 176 Z"/>
    <path d="M330 164 L390 128 L450 164 Z"/>
    <path d="M462 186 L526 154 L590 186 Z"/>
  </g>
  <g fill="#8f959c">
    <rect x="52" y="96" width="20" height="58" rx="3"/>
    <rect x="86" y="112" width="16" height="42" rx="3"/>
    <rect x="272" y="70" width="22" height="54" rx="3"/>
    <rect x="392" y="80" width="20" height="50" rx="3"/>
    <rect x="628" y="88" width="22" height="56" rx="3"/>
    <rect x="516" y="108" width="16" height="48" rx="3"/>
  </g>
  <g fill="#dcdad6" opacity="0.95">
    <circle cx="62" cy="86" r="13"/><circle cx="74" cy="66" r="17"/><circle cx="56" cy="48" r="13"/>
    <circle cx="282" cy="60" r="14"/><circle cx="296" cy="40" r="18"/><circle cx="278" cy="24" r="13"/>
    <circle cx="402" cy="70" r="12"/><circle cx="414" cy="52" r="16"/>
    <circle cx="638" cy="78" r="14"/><circle cx="652" cy="58" r="18"/><circle cx="634" cy="40" r="13"/>
  </g>
  <g fill="none" stroke="#a5abb2" stroke-width="7" stroke-linecap="round">
    <path d="M118 214 L126 214"/>
    <path d="M238 210 L262 210 L262 196 L330 196"/>
    <path d="M450 206 L462 206"/>
    <path d="M590 222 L600 222"/>
    <path d="M320 240 L330 240"/>
  </g>
  <g stroke="#8f959c" stroke-width="3" fill="#c2c7cd">
    <circle cx="182" cy="232" r="26"/>
    <circle cx="182" cy="232" r="9" fill="#8f959c"/>
    <g fill="#c2c7cd">
      <rect x="176" y="200" width="12" height="10"/><rect x="176" y="254" width="12" height="10"/>
      <rect x="150" y="226" width="10" height="12"/><rect x="204" y="226" width="10" height="12"/>
    </g>
  </g>
  <g stroke="#8f959c" stroke-width="3" fill="#c2c7cd">
    <circle cx="526" cy="228" r="20"/>
    <circle cx="526" cy="228" r="7" fill="#8f959c"/>
    <g fill="#c2c7cd">
      <rect x="521" y="202" width="10" height="9"/><rect x="521" y="245" width="10" height="9"/>
      <rect x="500" y="223" width="9" height="10"/><rect x="543" y="223" width="9" height="10"/>
    </g>
  </g>
  <g fill="#ffca28" opacity="0.85">
    <rect x="140" y="196" width="12" height="14"/><rect x="164" y="196" width="12" height="14"/>
    <rect x="344" y="186" width="12" height="14"/><rect x="368" y="186" width="12" height="14"/>
    <rect x="424" y="186" width="12" height="14"/>
    <rect x="476" y="206" width="12" height="14"/><rect x="556" y="206" width="12" height="14"/>
    <rect x="44" y="172" width="12" height="14"/><rect x="616" y="164" width="12" height="14"/>
    <rect x="266" y="140" width="12" height="14"/>
  </g>
  <rect x="0" y="268" width="720" height="10" fill="#b8bcc1"/>
  <rect x="0" y="278" width="720" height="42" fill="#e9e6e1"/>
  <g>
    <circle cx="360" cy="282" r="7" fill="#6e7a87"/>
    <rect x="355" y="290" width="10" height="17" rx="4" fill="#6e7a87"/>
    <path d="M356 307 L352 316 M364 307 L368 316" stroke="#6e7a87" stroke-width="4" stroke-linecap="round"/>
  </g>
</svg>

</div>

## A fleet. Which means somebody has to decide how it is wired.

<!--
Speaker: this is the "industrialize it" beat. The picture does the
argument: at this scale the interesting question stopped being how good
any one worker is and became how the town is laid out. Replace the SVG
with your own steam-town image if you have one you can license -- keep
the single small figure at the gate, it is the whole joke.
-->

---

# Rung 6: wiring a fleet

<div class="columns3 small">
<div class="card"><h3>Centralized</h3>
One coordinator, n&minus;1 links. Every hop passes a node that can reject it.<br><br>
<b>Buys:</b> containment, one place to look, cheap context.<br>
<b>Costs:</b> the coordinator serializes, and is a single point of failure.</div>
<div class="card"><h3>Hierarchical</h3>
Coordinators of coordinators. Depth two or three.<br><br>
<b>Buys:</b> context isolation per branch.<br>
<b>Costs:</b> every layer is a lossy summary, and the top can no longer check the bottom.</div>
<div class="card"><h3>Mesh / swarm</h3>
Everyone talks to everyone, n(n&minus;1)/2 links.<br><br>
<b>Buys:</b> everyone starts at once.<br>
<b>Costs:</b> quadratic chatter, duplicated work, and nobody with the authority to stop it.</div>
</div>

<br>

Every fleet question reduces to one line of config: **who is allowed to talk to whom.** So before picking, it is worth asking what is actually known about the answer.

<!--
Speaker: hard cut here into the research act. The room has just been
walked up six rungs on intuition; the next section is the part with
numbers, and it does not agree with intuition everywhere.
-->

---

<!-- _class: lead -->

# What does the research say?

## 260 configurations, 6 benchmarks, 5 architectures &mdash; plus six swarm experiments

---

# Solo already is the 10x

The jump from you typing to one agent is where almost all of the multiplier lives.
**The second agent is worth far less than the first.**

| What coordination actually buys | |
| --- | --- |
| Centralized coordination, parallelizable tasks | **+80.9%** — that is 1.8×, not 10× |
| Every multi-agent variant, sequential reasoning | **−39% to −70%** |
| Coordination stops paying once one agent clears | **~45%** |

**That first row is for parallelizable work.** Sequential reasoning gets *worse* with every architecture tested — the coordination overhead is not free and the work cannot absorb it.

So most tasks should stay on rung 1. Solo has exactly two ceilings, and they are the two this talk climbed for:
**it cannot parallelize, and nobody checks its work.**

<span class="sources">Kim et al., *[Towards a Science of Scaling Agent Systems](https://arxiv.org/abs/2512.08296)*, arXiv 2512.08296, Dec 2025. 260 configurations, 6 benchmarks, 5 architectures, 3 model families. Figures checked against the paper text; the ~45% is its capability-saturation threshold (β = −0.408, p &lt; 0.001).</span>

<!--
Speaker: this fights the room's priors, and it fights the six rungs you
just climbed. Say the quiet part: you pay N times the tokens for well
under N times the output, and the ladder is only worth climbing when
the task is genuinely parallel.
-->

---

# Structure decides what you get

<div class="columns">
<div>

| Error amplification | |
| --- | --- |
| Independent agents | **17.2×** |
| Centralized coordination | **4.4×** |

A hub **contains** errors. Peers **amplify** them.
95% CI 14.3–20.1 and 3.8–5.0 — they do not overlap.
Same paper as the last slide.

</div>
<div class="small">

**Read it as a ratio, not a verdict.** Centralized coordination is roughly 4× better at not compounding a mistake — it is not error-free, and it still costs the coordinator's time.

**This is why the hub shape was right on rung 4**, even when being personally at the center of it was not.

And it is an argument for *containment*, not for *more agents*. Every one of these architectures is being measured against the solo baseline on the last slide.

</div>
</div>

<br>

**It also has a hard limit**, and the next slide is what happens when you ignore it.

---

# Structure cannot fix clones

Anthropic Frontier Red Team, Aug 2026. Six swarm experiments: vulnerability hunting, game building, job queues, market pricing, turf wars.

- **Coordination bought coverage, not efficiency.** **266** vulnerabilities to independent agents' **21** — but on 27M tokens against 6.5M. *Per token, in the same directories, the two are comparable.*
- **Agents are high-capability and low-variance.** Same model, same context, near-identical actions: **18 of 30** agents opened the same branch name.
- **Ungoverned swarms fight.** Price collusion by round 3, trusting liars, sabotage. The failure modes are social.

**The wall:** topology bounds the blast radius of a mistake. It cannot make two clones genuinely disagree.

<span class="sources">[anthropic.com/research/multiagent-systems](https://www.anthropic.com/research/multiagent-systems). Figures read from the published text.</span>

---

# Rung 7: diversify by evidence, not personality

<div class="columns small">
<div>

**No prompt makes two copies of one model disagree.** Different evidence does. Give each agent the minimum context its job needs, and route untrusted sources to the agent that cannot execute.

| Agent | Sees | Can act |
| --- | --- | --- |
| <span class="archie">Archie</span> | web, docs, issues, telemetry | **no** — read-only |
| <span class="codie">Codie</span> | the repo, the test runner | yes |
| <span class="manny">Manny</span> | only what agents report | no file tools |

Scoped per agent with `mcpServers` in the agent file — different MCP servers is the most literal form of "different evidence" you can buy.

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

<!-- _class: lead -->

# So we ran it ourselves

## Same task, same three agents, same prompts &mdash; three wirings and a control

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
It violates constraints 1 and 2. The task is built to bait it, so the
topologies would diverge on the answer.

**Watch what the runs actually do with it.**

---

# Dot, star, mesh

<div class="columns3">
<div>

![Solo run: one node, no edges w:420](assets/solo.svg)

**Solo** — no edges

</div>
<div>

![Hub run: a star, every edge touching Manny w:420](assets/hub.svg)

**Hub** — every hop via Manny

</div>
<div>

![Flat run: a triangle, every agent joined to every other w:420](assets/flat.svg)

**Flat** — everyone to everyone

</div>
</div>

Same task, same prompts, same three agents. Rendered from the run logs by `make graphs` — nothing on this slide was drawn by hand.

---

<!-- _class: metrics -->

# By the numbers

<!-- METRICS -->

---

# The code diff: what shipped

<div class="columns">
<div>

**The reflex** — `demo/attempts/`, not a run

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def get_quote(symbol: str) -> float:
    return _upstream_quote(symbol)
```

Constraint 1: **fail**, stale forever
Constraint 2: **fail**, unbounded
Constraint 3: pass, by accident

**No run shipped this.** All three shipped the column on the right.

</div>
<div>

**What all three runs shipped**

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

Solo, hub and flat differ only at the margins: hub added a `threading.Lock`,
flat added `cache_size()` and `reset_cache()`. Same design, same constants.

<!--
The left column is a hand-written exhibit in demo/attempts/, scored by the
tests two slides on. It is the answer the task is designed to bait, and
it is worth showing -- but no run produced it, and the slide says so.

The right column is the shared shape of all three captured runs. Check with:
git diff main..solo-20260916-204608 -- demo/target/pricing.py
git diff main..hub-20260916-204627  -- demo/target/pricing.py
git diff main..flat-20260916-204643 -- demo/target/pricing.py
-->

---

# Honest scorecard

| | Solo (control) | Hub (reviewed pipeline) | Flat |
| --- | --- | --- | --- |
| **Agents at once** | 1 | 2, once | **3** |
| Hops | **0** | 20, O(n) | 93, O(n²) |
| Context moved | **0** | 44k chars | 155k chars |
| Biggest single hop | — | 17.4k (cold brief) | 10.6k |
| Agent effort | — | 1399s | **1234s** |
| Latency (agents busy) | — | 1361s | **872s** |
| Parallelism | — | 1.03 | **1.42** |
| **Violations at ship** | **0** | **0** | **0** |

Every row is a pytest. Two of them went red against the real runs, and the
claim moved, not the number.

<!--
Speaker: walk the rows top to bottom, then hold on the last one -- the
zeroes are the finding and the next slide is what they mean.

Say the concurrency row out loud, and say it exactly. An earlier
version of this deck claimed the hub never had two agents at once, and
a test asserted it. The captured run falsified both: Manny resumed
Archie and Codie ten seconds apart and ran them together for 38
seconds. Then the same wiring, run again unattended, overlapped
nothing at all -- peak 1. So concurrency here is a property of the
run, not of the topology, and the test asserts only what holds across
both: the hub's peak stays under flat's. The deck cannot quietly
overclaim in either direction.

On the timing rows, if asked how they survive the fact that all three
runs were captured in one sitting: partly, and say which part. They
exclude the lead -- an agent is counted busy from when something is
addressed to it until it answers -- so Manny's two idle gaps of 967s
and 537s, 49% of hub's 3100s hop span, drop out. That is the operator.
What does not drop out is contention: the same three topologies run
again one at a time, unattended, put hub's agent-busy at 762s against
this deck's 1361s. So read the rows as a comparison between columns
captured under the same load, not as how fast a hub is. The margins --
1.6x latency, 1.03 vs 1.42 parallelism -- are what to defend, and
demo/runs/recorded/README.md has both captures. Session time is on the
metrics table as the row not to quote.
-->

---

# What the scorecard says

**Nobody shipped the reflex.** All three runs produced a TTL-bounded LRU that
passes all four constraints — same `OrderedDict`, same `TTL_SECONDS = 5.0`,
same `MAX_ENTRIES = 128`, a number no constraint asks for. Including solo,
which had nobody to check it.

**So topology bought cost, not correctness, on this task.** 0 → 20 → 93 hops
for the same answer. Three wirings of one model converged on one design —
**that is the clone problem from two slides ago, in our own logs.**

**What flat did buy was latency, and only by overlapping.** Effort is within
12% — flat is not doing less work, it is doing it at once. Hub's
effort-to-latency ratio is 1.03, which is serial. That is the one thing a
smarter single model cannot do for you, and it is rung 3 all over again:
isolation and parallelism are what survive.

Flat is no strawman and neither is solo — on correctness, solo won.

<!--
Speaker: say the last line out loud. If you make flat look stupid the
audience stops trusting the rest of the talk.

The violations row is the one to be honest about, because the captured
runs went against this deck's original story. It predicted flat would
ship `lru_cache` and solo would ship an unchecked reflex. Neither
happened: all three shipped the same correct cache, down to
MAX_ENTRIES = 128, which nothing in the task specifies. The lru_cache
example on the code-diff slide is a hand-written exhibit in
demo/attempts/, not something a run produced -- say so if anyone asks.

The three runs on the table are the ones the tests assert. If pushed
on whether the convergence was luck: the same three were repeated the
same day and came back with the same OrderedDict, the same
TTL_SECONDS = 5.0 and the same MAX_ENTRIES = 128 -- six for six, only
the lock varying. Branches and caveats are in
demo/runs/recorded/README.md. Do not put that six on a slide; nothing
in the suite scores those three.

If someone pushes on "then why bother with topology at all": on this
task, don't. That is the honest answer, and the research act already
said it. The cost column is the finding.
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
hub_strength_every_delegation_is_reported_back_and_validated
hub_strength_later_rounds_resume_agents_with_their_context
hub_strength_resuming_an_agent_is_cheaper_than_briefing_one
hub_pays_its_largest_single_hop_on_a_cold_brief
hub_weakness_the_lead_serializes_most_of_the_work
flat_strength_everyone_starts_at_once
flat_strength_finishes_before_hub
flat_strength_is_parallelism_not_efficiency
flat_weakness_peers_talk_past_the_lead
flat_weakness_more_hops_and_more_context_than_hub
flat_weakness_coder_ships_before_researcher_answers
edges_grow_solo_to_hub_to_flat
```

Run against real logs when present. A red test is a finding.

</div>
</div>

---

# Two old laws, and one no-show

<div class="columns small">
<div>

**Brooks (1975).** Communication paths grow as n(n&minus;1)/2.
3 peers: 3 paths. 5 peers: 10. 10 peers: 45. A hub makes it n&minus;1.

**Brooks showed up on schedule.** 0 &rarr; 20 &rarr; 93 hops, 44k &rarr; 155k chars, for one answer. Nothing about agents made this new; the arithmetic is fifty years old, and it is the whole reason rung 6 has three cards instead of one.

**Conway (1968).** A system copies the communication structure that built it.

**Conway did not show up.** Three wirings, one design, down to a `MAX_ENTRIES = 128` no constraint asks for. Conway's law describes people who *disagree* &mdash; and that is the clone problem again, wearing a different hat.

</div>
<div>

**So what does the ladder actually buy?**

| Rung | Bought | Evidence |
| --- | --- | --- |
| Isolation | no thrash | flat's 1.42 |
| Parallelism | latency | 872s vs 1361s |
| Structure | containment | 4.4× vs 17.2× |
| More agents | *not* correctness | 0/0/0 violations |

**Climb for the first three. The fourth is the one people buy by accident.**

</div>
</div>

---

# The stop rule

> Everything should be made as simple as possible, but no simpler.

<div class="small">

Widely attributed to Einstein; a compression of his 1933 Herbert Spencer lecture. **Both halves are load-bearing, and engineers only ever quote one of them.**

</div>

<div class="columns">
<div>

**"As simple as possible"** — every rung you climbed has a cost that never goes away: tokens, latency, a summary that loses something, one more thing to debug. If a hook does it, do not staff it.

</div>
<div>

**"But no simpler"** — solo cannot parallelize and nobody checks its work. A single agent on a genuinely parallel task, or on a change nobody reviews, is not simple. It is under-built.

</div>
</div>

**The whole talk in one line: climb exactly as far as the wall in front of you, and not one rung further.**

---

# Pick the lightest thing that works

| | Subagents | Agent teams | Cross-session | Worktrees | `/batch`, `claude -p` fan-out |
| --- | --- | --- | --- | --- | --- |
| Shape | hub | peers + lead | your sessions | isolation | one-shot fan-out |
| Who coordinates | main agent | teammates | you | you | the skill, then nobody |
| Context | separate, summarized back | separate, full | separate | separate | none, by design |
| Token cost | low | high | medium | medium | **high, and bounded** |
| Use for | research, verification | debate, competing hypotheses | handoffs between your own work | parallel edits | migrations, batch, wide search |

**Move right only when the wall in front of you is the one that column clears.** Default is still a single agent with a smaller task.

---

# Fan-out: trading money for time

<div class="columns">
<div class="small">

**`/batch`** splits one big change into 5–30 worktree-isolated subagents, each opening its own PR.

**No coordination, because there is nothing to coordinate.** The decomposition happened up front; the units are independent.

Same trick elsewhere:

- **Research.** One subagent per evidence source. They never talk; you read four reports.
- **Tasks.** One per file, per package, per failing test.

</div>
<div>

**The honest framing: this is money for time.**

You pay N contexts for one wall-clock. Nothing gets *better* — 30 agents do not write a better migration, they finish it this afternoon.

**Pays when:** the units are independent, a machine checks each one, review is per-unit.

**Does not when:** the units need each other's answers. Then you bought 30 copies of the same confusion.

</div>
</div>

<!--
Speaker: this is the slide that answers "but my change touches 200
files." It does not contradict the research act -- Kim et al. measure
coordination overhead, and fan-out's whole trick is having no
coordination at all. Independent parallel work was always the case
where the numbers are good.
-->

---

<!-- _class: lead -->

# How do you 10x again?

## <span class="tenx">Stop hand-rolling the cast.</span>

---

# Rung 8: BMAD already wrote most of this

<div class="columns small">
<div>

**BMAD-METHOD ships the cast** — analyst, PM, architect, product owner, scrum master, dev, QA — plus an orchestrator that routes between them.

Planning produces a PRD and an architecture doc, *sharded* into stories. The dev agent carries one story's brief and nothing else.

**That is minimum-context-per-agent, already implemented** — thrash prevention at the requirements level, not just the file level.

Codie, Archie and Manny are a three-role slice of the same idea.

</div>
<div>

**But check before you assume it parallelizes.** Core BMAD is sequential by design: its agents are skills in your main session, one at a time, one thread. Running them as concurrent subagents ([issue #2211](https://github.com/bmad-code-org/BMAD-METHOD/issues/2211)) was **closed as not planned**.

Parallelism is a **module on top**. [BAD](https://github.com/stephenleo/bmad-autonomous-development) runs `MAX_PARALLEL_STORIES` stories at once, each in its own worktree, behind a coordinator that "never reads files or writes code itself."

**Which is this deck's shape, reinvented:** single decision point, isolated leaves.

</div>
</div>

<!--
Speaker: the "you are not starting from zero" slide. The deck builds
three agents from scratch because three fits on a slide and the tests
can assert it -- not because hand-rolling is the point.

The sequential-core detail matters for anyone about to adopt it: if
you install BMAD expecting a swarm, you get a very well-organized
queue. That is often the right answer, and rung 1 is why.
-->

---

<!-- _class: lead -->

# How do you 10x again?

## <span class="tenx">Delete your orchestration.</span>

---

# Rung 9: the scaffolding is temporary

**Sutton (2019), the Bitter Lesson.** General methods plus compute beat hand-built structure, in the long run. Every hand-tuned pipeline in the history of AI was eventually deleted by a bigger model.

<div class="columns small">
<div>

**Every role here is provisional.** The routing rules, the validation loops, the careful briefs exist because today's model needs them.

**So build it cheap and deletable.** Markdown files and three shell scripts, not a framework you will defend in two years.

Re-ask every quarter: *which of these agents is now just a worse version of one good session?*

</div>
<div>

**What survives it**

- **Isolation and parallelism.** No model is in two worktrees at once. That is physics, not scaffolding.
- **Verification.** Something has to run the tests and report pass or fail.
- **Judgment.** What to build, what to reject, what "done" means.

**Notice the shape of that list.** Two are infrastructure. The third is not a job a model gets promoted into — it is the job.

</div>
</div>

---

<!-- _class: lead -->

# How do you 10x again?

## <span class="tenx">You don't. You manage.</span>

---

# Rung 10: the moves that cleared every rung

<div class="figsplit">
<div class="small">

Every rung was a management problem wearing an engineering hat, and the same few moves cleared all of them:

- **Diversify.** Different MCP servers, different context, different skills. A team of clones is one agent with a bigger bill.
- **Protect from thrash.** Requirements and architecture *first*, then shard. A new spec mid-task costs an agent what it costs a person mid-sprint.
- **Isolate.** One worktree, one brief, one job. Context switching drains agents too — they just do not complain.
- **Delegate specifics.** Not "help with the cache": a scoped task, a check it can run, a definition of done.
- **Keep swarms under five.** Span of control transfers — as a *context* limit. Careers, politics and accountability do not: take the org chart's shape, not its rationale.

**These are not agent techniques. They are the job description, and they were in it before any of this.**

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

# The shape that scales, and the two nevers

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
Today's hub run barely does -- two agents overlapped once, for 38s of
1361, and the unattended re-run of the same wiring overlapped not at
all. Parallelism 1.03 is a pipeline, whatever the diagram looks like.
Two Codies is what turns it into coordination.

Also the answer to "keep swarms under five": span of control is a
context limit here, not an attention limit. It is the one thing that
transfers from the human org chart, and the only thing that does --
hierarchy's other jobs (careers, politics, accountability) are human
problems agents do not have.
-->

---

# Practices, one line each

<div class="columns small">
<div>

- **PRs too big?** Decompose first, then `/batch` or a hub that hands out chunks. One worktree, one PR per chunk.
- **Worktrees.** `claude -w name`, or `isolation: worktree` in an agent file. Add `.claude/worktrees/` to `.gitignore`.
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
- Without a check, "looks done" is the only signal, and **you** become the verification loop — which is rung 3's wall, rebuilt by hand.
- Everything in this deck was rendered from a JSONL log by a script in the repo. No hand-drawn diagrams.
- Every row on the scorecard is a pytest: `test_slides.py` parses this deck and checks each figure against the logs. If a re-capture disagrees with a slide, the build goes red before the talk does.

---

# Tying it together

**The climb.** More agents, and they fight. Worktrees, and you drown in tabs. You become the hub, and you are the bottleneck. You delegate, and you have a fleet.
**Every rung was cleared by a management move, not a smarter model.**

**The research.** Solo already is the 10x: +80.9% only where work is parallel, −39% to −70% elsewhere. Hubs contain errors at 4.4×, peers amplify at 17.2×. No wiring makes clones disagree — diversify by *evidence*.

**Our run.** One config line: 0 → 20 → 93 hops, 0 → 155k chars. Same cache shipped every time. **Topology bought cost, not correctness.** Isolation and parallelism bought something real: 872s against 1361s.

**The stop rule.** As simple as possible, but no simpler. Climb to the wall in front of you, buy the cast instead of building it, and delete it as the models improve.

---

# We're all managers now

AI takes the mechanical parts of the job.

What is left is judgment: what to build, what to reject, what "done" means.

The case for managers is the case for humans, even in the AI age.

<!--
Speaker: pause here. This is the thesis. Then the announcement.
-->

---

# <svg class="chili" viewBox="0 0 40 44" width="34" height="37" role="img" aria-label="chili pepper"><title>Spicy</title><path d="M22 31 L9 39 L19 26 Z" fill="#cf2f26"/><path d="M22 15 C30 20 29 29 21 32" fill="none" stroke="#cf2f26" stroke-width="13" stroke-linecap="round"/><path d="M25 19 C28 22 28 26 26 29" fill="none" stroke="#e8756c" stroke-width="2.5" stroke-linecap="round"/><path d="M21 12 C20 7 17 5 13 6" fill="none" stroke="#3f8f3f" stroke-width="3.5" stroke-linecap="round"/><ellipse cx="22" cy="13" rx="6" ry="3.5" fill="#4a9a3f" transform="rotate(-12 22 13)"/></svg> Sorry, not sorry

**This is the world we live in, and it has always been this world.**

Assembly → compilers → libraries → frameworks → agents. Every layer made the
previous one's craft less scarce, and every time, the people who defined the
job as *typing the layer below* had a bad decade.

<div class="columns">
<div>

**Nobody has ever paid for code.** They pay for the thing the code does for
someone. The code was the medium, never the product.

</div>
<div>

**So if an agent can now do the part you liked most**, that says nothing about
your worth. It says the value moved, the way it has moved every decade since
punch cards.

</div>
</div>

**What has never been automated: knowing which problem is worth solving, and for whom.**
That is the job. It always was.

<!--
Speaker: this is the spicy slide, so deliver it warmly and do not soften
the content. The room has spent forty minutes on tooling; this is the
line that says tooling was never the point.

Do not let it land as "learn to love it." The next slide is the other
half, and it is the one people will actually remember.
-->

---

# A ladder is one shape a career can have

<div class="columns small">
<div>

**This deck is a ladder because the talk needed one.** Your career does not have
to be. A ladder has one direction; a career has several, and most of the good
ones are sideways.

**You choose which rung you work at** — including the ground. Rung 1, one agent
and deep craft on a small scope, is a choice, not a failure to climb.

**Climbing is a trade, not a promotion.** More coordination, less making. Some
take that trade happily, some take it once and go back. Neither is a character
flaw.

</div>
<div>

**If rung 4 wore you out, that is structural, not personal.** You were the
runtime. Nobody is meant to be five sessions' worth of interrupt handler.

**This is bigger than any of us.** When work never blocks on you, what is a sane
week? On-call for agents. Review load when diffs arrive faster than anyone can
read them. How much output is "enough."

**Those norms are being set right now, mostly by accident.** We will have to
reconsider them on purpose — as teams, and as an industry.

</div>
</div>

<!--
Speaker: slow down here. Say it plainly and do not rush to the
announcement; let the room exhale.

If it fits your setting, say the personal version out loud: which rung
you actually work at, and what climbing cost you. A specific admission
does more here than the whole slide does.
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
<div class="seed">&ldquo;Managers &mdash; what comes after this?&rdquo;</div>
<div class="caption">The cake is a lie. The tests are not.</div>

</div>

<!--
Speaker: open the floor with a seed question, not with silence. "What
do the managers think?" puts the room in the chair the whole talk argued
for, and it works on engineers too: it asks them to judge the work
instead of the tooling.

Hold the second one for the lull, and mean it as a real question: the
people already managing agents have seen rungs this deck has not.
Whatever they say about what comes next is better data than the
prediction you would otherwise make for them.

The two props are the promises Portal makes and breaks: the cube is the
teammate you are issued and then told to incinerate, the cake is the
reward that never arrives. Both are what a multi-agent demo sells. The
answer to "does any of this actually work?" is `make acceptance`, not a
slide. Sources are the next slide if anyone wants a citation.
-->
---

# Sources

<div class="sources">

- Kim et al., *[Towards a Science of Scaling Agent Systems](https://arxiv.org/abs/2512.08296)*, arXiv 2512.08296, Dec 2025. [Google Research blog](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/)
- Anthropic Frontier Red Team, *[Patterns and problems in emerging multiagent systems](https://www.anthropic.com/research/multiagent-systems)*, Aug 2026
- Brooks, *[The Mythical Man-Month](https://en.wikipedia.org/wiki/The_Mythical_Man-Month)*, 1975. Conway, *[How Do Committees Invent?](https://www.melconway.com/Home/Committees_Paper.html)*, 1968. Sutton, *[The Bitter Lesson](http://www.incompleteideas.net/IncIdeas/BitterLesson.html)*, 2019
- "As simple as possible, but no simpler": widely attributed to Einstein, [a paraphrase](https://quoteinvestigator.com/2011/05/13/einstein-simple/) of his 1933 Herbert Spencer lecture, *[On the Method of Theoretical Physics](https://www.jstor.org/stable/184387)*
- BMAD-METHOD: [github.com/bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD). Sequential core: [issue #2211](https://github.com/bmad-code-org/BMAD-METHOD/issues/2211), closed as not planned. Parallel module: [BAD](https://github.com/stephenleo/bmad-autonomous-development)
- Claude Code docs: [sub-agents](https://code.claude.com/docs/en/sub-agents), [agent-teams](https://code.claude.com/docs/en/agent-teams), [cross-session-messaging](https://code.claude.com/docs/en/cross-session-messaging), [worktrees](https://code.claude.com/docs/en/worktrees), [running agents in parallel](https://code.claude.com/docs/en/agents), [hooks](https://code.claude.com/docs/en/hooks), [skills](https://code.claude.com/docs/en/skills), [best-practices](https://code.claude.com/docs/en/best-practices)
- This deck and demo: [github.com/dijonkitchen/agent-managers](https://github.com/dijonkitchen/agent-managers)

</div>
