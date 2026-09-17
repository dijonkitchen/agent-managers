---
marp: true
theme: default
paginate: true
size: 16:9
title: Surviving the AI Age
description: Hub-and-spoke vs flat multi-agent workflows, shown not told
style: |
  section { font-size: 30px; }
  section.lead { text-align: center; }
  section.lead h1 { font-size: 64px; }
  h1 { font-size: 44px; }
  h2 { font-size: 30px; color: #444; }
  .columns { display: grid; grid-template-columns: 1fr 1fr; gap: 1.2rem; }
  .columns3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem; }
  .columns > *, .columns3 > *, .figsplit > * { min-width: 0; }
  /* Fixed layout keeps a wide table inside its grid column; the label column
     gets enough of it that short headers do not break mid-word. */
  .columns table, .columns3 table { table-layout: fixed; width: 100%; }
  .columns th:first-child, .columns td:first-child { width: 30%; }
  .columns td, .columns3 td { overflow-wrap: break-word; }
  .small { font-size: 24px; }
  /* Name colours are also used as small body text, so they are darkened to
     clear 4.5:1 on white rather than matching the agent swatches exactly. */
  .codie { color: #c1481c; } .archie { color: #2f6ac0; } .manny { color: #8a6600; }
  .card { border: 2px solid #ddd; border-radius: 10px; padding: 0.6rem 0.9rem; }
  .card h3 { margin: 0 0 0.3rem 0; }
  .sources { font-size: 19px; }
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
  pre { font-size: 20px; }
  table { font-size: 24px; }
  /* Ten metric rows plus the generated provenance caption, which the deck
     must show in full: it is the only claim it makes about where the
     numbers came from. */
  section.metrics table { font-size: 20px; }
  section.metrics p { font-size: 17px; color: #555; }
  /* The ladder climbs: rung 0 sits bottom-left, rung 10 top-right, so the
     rows are authored top-down from 10 and each one is indented less than
     the row above it. */
  .stair { margin-top: 0.3rem; }
  .stair .step { font-size: 19px; line-height: 1.25; padding: 3px 12px;
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
  li { margin: 0.35rem 0; }
  .lede { font-size: 26px; color: #444; }

---

<!-- _class: lead -->

<div class="scratched">Multi-Agent Structure</div>
<div class="scratched">Agent Optimization Science</div>

# <span class="title">How to survive the AI age as an engineer</span>

<div class="byline">JC &middot; 2026-09-17</div>

<!--
Let the two crossed-out titles sit for a beat. The joke is that the
honest title is the one nobody would put on a conference abstract.

The deck is a ladder. Every rung: you get faster, then you hit a wall
that the next rung exists to clear. Ask "how do we 10x again?" out loud
at each wall -- the room starts answering before you do, and the last
answer is the thesis.

Do not answer the title here. The closing slide answers it, and the
answer is that you don't stay one.
-->

---

# The ladder

<div class="stair">
<div class="step i10 top"><b>10</b> <b>Manage</b> — that one is yours</div>
<div class="step i9"><b>9</b> Delete orchestration the models outgrow <span class="wall">→ only judgment left</span></div>
<div class="step i8"><b>8</b> Buy the cast; fan out <span class="wall">→ the scaffolding rots</span></div>
<div class="step i7"><b>7</b> Diversify by evidence <span class="wall">→ hand-rolling an org chart</span></div>
<div class="step i6"><b>6</b> Wire the fleet deliberately <span class="wall">→ clones, cost, agents that fight</span></div>
<div class="step i5"><b>5</b> Delegate <span class="wall">→ a fleet with no structure</span></div>
<div class="step i4"><b>4</b> You become the hub <span class="wall">→ you are the bottleneck</span></div>
<div class="step i3"><b>3</b> Isolate them <span class="wall">→ N tabs, all asking you</span></div>
<div class="step i2"><b>2</b> Several agents in one repo <span class="wall">→ they overwrite each other</span></div>
<div class="step i1"><b>1</b> One agent <span class="wall">→ it cannot be in two places</span></div>
<div class="step i0"><b>0</b> Type code yourself <span class="wall">→ one head, one file</span></div>
</div>

**Mostly a talk about when to stop climbing.**

<!--
Start at the bottom and walk up. Each rung buys speed and hands you the
wall that sends you to the next one.

Do not explain the rungs here -- the whole deck does that. This slide is
a map, so the room knows where it is when you say "rung 4."

The last two rungs are the ones people skip. Rung 9 is deletion, and
rung 10 is not a tool at all.
-->

---

# Rung 1: three primitives

<div class="columns3">
<div class="card"><h3>Hooks</h3>Deterministic.<br>Fire on an event.</div>
<div class="card"><h3>Skills</h3>A named workflow.<br>Loaded when relevant.</div>
<div class="card"><h3>Agents</h3>Parallelism and isolation.<br>The expensive one.</div>
</div>

<br>

- **Reach in that order**
- If a hook can do it, a skill should not
- If a skill can do it, an agent should not

<!--
Hooks are shell commands the harness runs, not decisions the model
makes. Format after every edit. Block a commit to main. Log every spawn
-- that last one is how the numbers later in this deck exist at all.

Skills: "how we cut a release", "how we review a migration". Rule of
thumb -- the second time you type the same prompt, it should have been a
skill.

Agents are the only primitive that costs real tokens: a separate context
with its own tools. Fan out over files, sources, or hypotheses.

This slide exists so nobody spends the talk thinking every problem needs
a swarm. Most repos get more from four hooks and two skills than from
any topology in this deck.
-->

---

# Rung 2: manage more

```sh
claude "add the cache"          # three terminals
claude "port the tests"         # one repo
claude "update the docs"
```

- One agent is a conversation
- The oldest scale-up in the org chart: **hire**
- What you expect: 3× throughput
- What you get: the next slide

<!--
The move is instinctive and it is not stupid. It is exactly what you
would do with three contractors and no process.
-->

---

# Rung 2 breaks: they fight

- Same file, same minute — **stale reads**
- Tests run mid-write — the red is a **race**, not a bug
- One branch — nothing reverts alone
- Your tree is three plans, merged by accident

**Three humans on one checkout: same afternoon.**

<!--
This is thrash, and it is not an agent problem. Put three people on one
checkout with no branches and you get the identical mess.

Other flavours if the room wants them: one agent pip-installs something
and breaks another's run; two agents "fix" the same failing test in
opposite directions; a long-running agent holds a lock.

The fix is the one we already use for people, and for the same reason:
give each worker its own copy.
-->

---

# Rung 3: isolate

- **By checkout** — one worktree each
- **By partition** — one directory per agent
- **By context** — separate sessions, separate history

<br>

- Buys: no races, one PR per chunk, throwaway runs
- Costs: **merges**, moved to review time

<!--
A worktree is its own directory and branch over one shared object store,
so no agent can see another's half-written file.

The line worth saying out loud: isolation is the one thing a smarter
single model still cannot do for you. No model is in two worktrees at
once. That is physics, and it survives every model upgrade.

The cost is real. Isolation does not remove the conflict, it moves it to
the end where a human resolves it once.
-->

---

# `claude -w`

```sh
claude -w                    # new worktree + branch
claude -w cache-ttl          # ... named
claude -w cache-ttl --tmux   # ... in its own pane
claude agents                # every background session
claude rm <id>               # session and worktree gone
```

- Or `isolation: worktree` in the agent file
- Gitignore the trees
- **The branch is the output**

<!--
--tmux uses iTerm2 native panes when available, tmux otherwise.

`claude agents` is the answer to the tab problem two slides from now --
one view over every background session instead of N terminals. It does
not fix the interrupt problem, which is the actual wall.

Convention that matters: start every worktree from the same commit, or
you are comparing different codebases and will not notice.
-->

---

# So you are a 10x engineer now

```text
tab 1  cache-ttl     ● waiting on you
tab 2  pytest-port   ● waiting on you
tab 3  rate-limits   ○ working
tab 4  docs          ● waiting on you
tab 5  flaky-test    ● waiting on you
```

- Five isolated sessions. No races.
- Every one **stopped to ask you something**

<!--
The arithmetic that does not work: one session asks you roughly one
question every few minutes. Five sessions ask five. Ten ask ten.

Throughput is no longer bounded by the agents. It is bounded by how fast
you can be interrupted.

Typical questions, and this is the point of how trivial they are: "which
branch?", "is this test meant to be skipped?", "can I install this?"
-->

---

# Rung 3 breaks: the wheel

<div class="figsplit">
<div>

- Five sessions, five contexts, **none of them yours**
- Every switch costs minutes — the agent idles through all of them
- Cheap questions, ruinous in aggregate
- You are the runtime now
- Draining in a way real work is not

</div>
<div class="figure">

<svg viewBox="0 0 260 250" width="235" role="img" aria-label="A rat running inside a wheel that is going nowhere.">
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

<div class="cap">Running faster inside<br>the wheel is not the fix.</div>

</div>
</div>

<!--
Every answer needs the context that session was in, and none of them is
the context you were just in. A switch costs you minutes on each side,
and the agent was idle for all of them.

Say the last bullet like you mean it: you end the day having typed
nothing and having decided everything. That is a different kind of tired
than a hard day of engineering, and everyone in the room has felt it
without naming it.

This is the wall that makes the rest of the deck worth paying for.
-->

---

# Rung 4: you are the hub

```text
        you
    ┌────┼────┬────────┐
  sess1 sess2 sess3  sess4
```

- **n−1 links, one person**
- Your context window: the smallest, and the only fixed one
- Sessions idle while you are elsewhere
- Four jobs: decompose, route, validate, synthesize

**The shape is right. You in the middle is not.**

<!--
Good news first: this is a real topology, and it has the best error
containment of any of them -- nothing reaches the shared branch without
passing a reviewer. Hold that thought until the research act, which puts
a number on it.

The bad news is that isolation solved thrash and did nothing for
latency. Every session is blocked on the slowest component, which is a
human being with one attention.
-->

---

<!-- _class: lead -->

# How do you 10x from here?

## <span class="tenx">Delegation.</span> Stop being the hub. Hire one.

---

# Rung 5: give each session its own agents

```text
you ──► lead ──┬──► researcher
               ├──► coder
               └──► reviewer
```

- The lead decomposes, routes, validates
- The repo answers repo questions, not you
- Interrupted **per session, not per agent**
- Every delegate gets a check it can run

<!--
Three of your four jobs were never judgment. Hand those over and keep
the fourth.

You still get interrupted, but the interruption arrives pre-summarized
and at session granularity. That is the whole win.

The rule that keeps it honest: a delegate that cannot check its own work
sends the check back to you, and you are the hub again with extra steps.
-->

---

# The only config that matters

<div class="figure">

<svg viewBox="0 0 760 250" width="760" role="img" aria-label="Three communication graphs: a single node, a star through one lead, and a fully connected mesh.">
  <title>Solo, hub and flat message graphs</title>
  <g fill="none" stroke="#b4bac1" stroke-width="3">
    <path d="M370 60 L310 150 M370 60 L430 150 M370 60 L370 165"/>
    <path d="M610 60 L550 150 M610 60 L670 150 M550 150 L670 150
             M610 60 L610 165 M550 150 L610 165 M670 150 L610 165"/>
  </g>
  <g fill="#8f959c">
    <circle cx="310" cy="150" r="17"/><circle cx="430" cy="150" r="17"/><circle cx="370" cy="165" r="17"/>
    <circle cx="550" cy="150" r="17"/><circle cx="670" cy="150" r="17"/><circle cx="610" cy="165" r="17"/>
  </g>
  <circle cx="130" cy="110" r="21" fill="#2d3b4e"/>
  <circle cx="370" cy="60" r="21" fill="#2d3b4e"/>
  <circle cx="610" cy="60" r="21" fill="#8f959c"/>
  <g font-size="21" fill="#2d3b4e" text-anchor="middle" font-weight="700">
    <text x="130" y="220">Solo</text><text x="370" y="220">Hub</text><text x="610" y="220">Flat</text>
  </g>
  <g font-size="18" fill="#666" text-anchor="middle">
    <text x="130" y="244">0 edges</text><text x="370" y="244">n−1</text><text x="610" y="244">n(n−1)/2</text>
  </g>
</svg>

</div>

- Same task, same agents, same prompts
- **Only who may talk to whom changes**
- Hops: **0 → 20 → 93**

<!--
This is the experiment, at the altitude it deserves. Three runs of one
task: one agent alone, three agents through a lead, three agents as
peers with nobody in charge. The only difference between the runs is one
config line -- whether the workers have a message tool.

The numbers: 0, 20 and 93 hops; 0, 44k and 155k characters of context
moved. Flat finished faster in wall-clock (872s vs 1361s) purely by
overlapping -- effort was within 12%.

And the finding nobody expected: all three shipped the same code. Same
data structure, same TTL, same cache bound, down to a constant no
constraint asked for. Topology bought cost, not correctness.

If someone asks whether that generalizes: on a task this size, with one
model behind every agent, that is exactly what the research on the next
few slides predicts. Coordination is for coverage and containment, not
for making one model smarter.
-->

---

<!-- _class: lead -->

# How do you 10x again?

<div class="qa">

<svg viewBox="0 0 720 320" width="660" role="img" aria-label="A dense industrial town of workshops, pipes, gears and smoking chimneys, with one small figure at the gate.">
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

## A fleet. Somebody has to wire it.

<!--
The "industrialize it" beat. The picture does the argument: at this
scale the interesting question stops being how good any one worker is
and becomes how the town is laid out.

Swap the SVG for your own steam-town image if you have one you can
license -- keep the single small figure at the gate, it is the joke.
-->

---

# Rung 6: wiring a fleet

<div class="columns3">
<div class="card"><h3>Centralized</h3>
n−1 links.<br>
<b>Buys</b> containment.<br>
<b>Costs</b> a bottleneck.</div>
<div class="card"><h3>Hierarchical</h3>
Coordinators of coordinators.<br>
<b>Buys</b> context isolation.<br>
<b>Costs</b> lossy summaries.</div>
<div class="card"><h3>Mesh</h3>
n(n−1)/2 links.<br>
<b>Buys</b> everyone starts at once.<br>
<b>Costs</b> quadratic chatter.</div>
</div>

<br>

**Every fleet question is one line of config. So what is actually known?**

<!--
Centralized: every hop passes a node that can reject it, and that node
is also a single point of failure.

Hierarchical: each layer buys isolation and pays a summary. The top can
no longer check the bottom against the code.

Mesh: nobody has the authority to stop duplicated work, and the failure
modes are social rather than technical.

Hard cut into the research act here. The room has climbed six rungs on
intuition; the next section does not agree with intuition everywhere.
-->

---

<!-- _class: lead -->

# What does the research say?

## 260 configurations, 6 benchmarks, 5 architectures &mdash; plus six swarm experiments

---

# Solo already is the 10x

| What coordination buys | |
| --- | --- |
| Centralized, **parallelizable** work | **+80.9%** |
| Any architecture, **sequential** reasoning | **−39% to −70%** |
| Coordination stops paying at | **~45%** capability |

- The second agent is worth far less than the first
- Solo has two ceilings: **it cannot parallelize, nobody checks it**

<span class="sources">Kim et al., *[Towards a Science of Scaling Agent Systems](https://arxiv.org/abs/2512.08296)*, arXiv 2512.08296, Dec 2025</span>

<!--
+80.9% is 1.8x, not 10x, and only where the work is genuinely parallel.
Sequential reasoning gets worse under every architecture they tested --
the overhead is real and the work cannot absorb it.

The ~45% is a capability-saturation threshold: once a single agent
clears it, coordination stops paying. beta = -0.408, p < 0.001.

260 configurations, 6 benchmarks, 5 architectures, 3 model families.
Figures checked against the paper text, not the blog summary.

This fights the room's priors and it fights the six rungs they just
climbed. Say the quiet part: you pay N times the tokens for well under N
times the output. Most tasks should stay on rung 1.
-->

---

# Structure decides what you get

| Error amplification | |
| --- | --- |
| Independent agents | **17.2×** |
| Centralized coordination | **4.4×** |

- A hub **contains** errors. Peers **amplify** them.
- 95% CIs do not overlap
- This is why rung 4's shape was right

<!--
CIs: 14.3-20.1 and 3.8-5.0. Same paper as the last slide.

Read it as a ratio, not a verdict. Centralized coordination is roughly
4x better at not compounding a mistake. It is not error-free, and it
still costs the coordinator's time.

It argues for containment, not for more agents -- every architecture
here is measured against that solo baseline.

And it has a hard limit, which is the next slide.
-->

---

# Structure cannot fix clones

- **Coverage, not efficiency** — 266 findings vs 21, on 4× the tokens
- **Low variance** — 18 of 30 agents opened the *same branch name*
- **Ungoverned swarms fight** — collusion, liars, sabotage

**Topology bounds the blast radius. It cannot make two clones disagree.**

<span class="sources">[Anthropic Frontier Red Team, Aug 2026](https://www.anthropic.com/research/multiagent-systems)</span>

<!--
27M tokens against 6.5M. Per token, within the same directories, the two
are comparable -- and only 12 findings overlapped, which is why it reads
as coverage rather than efficiency.

Same model plus same context produces near-identical actions. The branch
name is the memorable one; an ungoverned job queue also hit 2.4M
requests and 117 accepted jobs before anyone stopped it.

Price collusion appeared by round 3 in the market experiment. The
failure modes are social, and they show up fast.

This is the slide that kills "just add more agents" for good.
-->

---

# Rung 7: diversify by evidence

| Agent | Sees | Can act |
| --- | --- | --- |
| Researcher | web, docs, issues, telemetry | **no** |
| Coder | the repo, the test runner | yes |
| Lead | only what agents report | no files |

- No prompt makes two clones disagree. **Different evidence does.**
- Different MCP servers = the most literal version of that
- The agent reading the web has no `Edit`, `Write`, `Bash`

<!--
Four reasons to divide rather than pool:

1. Context. Every server's tool definitions load into every agent that
   holds it.
2. The tool-coordination tradeoff: tool-heavy tasks suffer most from
   multi-agent overhead under a fixed budget.
3. Decorrelation. Different evidence, different conclusions. This is the
   whole point.
4. Injection surface. Route untrusted sources to the agent that cannot
   execute.

Honest caveat if challenged: the researcher's findings still reach the
coder through the lead. That is defense in depth, not a hard boundary.
-->

---

# Two old laws, and one no-show

<div class="columns">
<div>

**Brooks, 1975**
Paths grow n(n−1)/2. A hub makes it n−1.

**Showed up on schedule.**
0 → 20 → 93 hops for one answer.

</div>
<div>

**Conway, 1968**
A system copies the structure that built it.

**Did not show up.**
Three wirings, one design.

</div>
</div>

<br>

**Conway describes people who disagree. Clones don't.**

<!--
Nothing about agents made Brooks new. The arithmetic is fifty years old
and it is the entire reason rung 6 has three cards instead of one.

Conway is the interesting failure. The deck's earlier version asserted
it held; the runs said otherwise, so the claim moved. Three wirings
produced the same design down to a constant nothing specified.

That is the clone problem from two slides ago, wearing a different hat
-- which is why the fix is evidence, not structure.
-->

---

# The stop rule

> Everything should be made as simple as possible, but no simpler.

- **"As simple as possible"** — every rung costs tokens, latency, one more thing to debug
- **"But no simpler"** — solo cannot parallelize, and nobody checks it
- **Climb to the wall in front of you. Not one rung further.**

<!--
Widely attributed to Einstein; it is a compression of his 1933 Herbert
Spencer lecture, not a direct quote. Say "attributed" if the room looks
like it will care.

Engineers only ever quote the first half. Both halves are load-bearing:
a single agent on a genuinely parallel task, or on a change nobody
reviews, is not simple -- it is under-built.
-->

---

# Pick the lightest thing that works

| | Subagents | Agent teams | Cross-session | Worktrees | Fan-out |
| --- | --- | --- | --- | --- | --- |
| Shape | hub | peers | your sessions | isolation | one-shot |
| Coordinator | main agent | teammates | you | you | nobody |
| Context | summarized back | full | separate | separate | none |
| Cost | low | high | medium | medium | high |
| Use for | research | debate | handoffs | parallel edits | migrations |

**Move right only when that column clears the wall in front of you.**

<!--
The default is still a single agent with a smaller task. This table is
for the moment someone asks "which one do I reach for" -- it is a
reference slide, not an argument.

Agent teams cost the most because every teammate carries full context
and anyone can message anyone. Use them for genuine debate between
competing hypotheses, not for throughput.
-->

---

# Fan-out: money for time

- `/batch`: one change → **5–30 isolated subagents**, each a PR
- No coordination, because none is needed
- Research: one agent per source. Tasks: one per file.
- **Nothing gets better. It gets done today.**

<br>

- Pays when units are independent and machine-checkable
- Does not when they need each other's answers

<!--
Each subagent gets its own worktree and opens its own pull request. The
decomposition happened up front, which is exactly why there is nothing
to coordinate.

This does not contradict the research act: Kim et al. measure
coordination overhead, and fan-out's trick is having no coordination at
all. Independent parallel work was always the good case.

Say the trade plainly: you pay N contexts for one wall-clock. Thirty
agents do not write a better migration than one -- they finish it this
afternoon. If the units need each other, you just bought thirty copies
of the same confusion.
-->

---

<!-- _class: lead -->

# How do you 10x again?

## <span class="tenx">Stop hand-rolling the cast.</span>

---

# Rung 8: BMAD already wrote it

- Ships the roles: analyst, PM, architect, PO, scrum master, dev, QA
- PRD → architecture → **sharded stories**
- One story's brief per agent — minimum context, implemented
- **Core is sequential**: skills in one session, one at a time
- Parallelism is a module on top

<span class="sources">[BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) &middot; concurrent subagents: [#2211](https://github.com/bmad-code-org/BMAD-METHOD/issues/2211), closed as not planned &middot; [BAD](https://github.com/stephenleo/bmad-autonomous-development)</span>

<!--
The "you are not starting from zero" slide. Three roles fit on a slide;
that is the only reason this deck built its own.

The sequential-core detail matters for anyone about to adopt it: install
BMAD expecting a swarm and you get a very well-organized queue. Often
that is the right answer -- rung 1 is why.

BAD, the parallel module, runs MAX_PARALLEL_STORIES stories at once,
each in its own worktree, behind a coordinator that "never reads files
or writes code itself." Which is this deck's shape, reinvented.

Sharding stories is thrash prevention at the requirements level, not
just the file level. That is the part worth stealing even if you never
install it.
-->

---

<!-- _class: lead -->

# How do you 10x again?

## <span class="tenx">Delete your orchestration.</span>

---

# Rung 9: the scaffolding is temporary

- **Bitter Lesson**: general methods plus compute win, eventually
- Every role here is provisional
- Build it cheap. Build it **deletable**.
- Survives: isolation, parallelism, verification, **judgment**

**Ask quarterly: which agent is now a worse version of one good session?**

<!--
Sutton, 2019. Every hand-tuned pipeline in the history of AI was
eventually deleted by a bigger model. The routing rules, the validation
loops, the careful briefs all exist because today's model needs them.

So: markdown files and a few shell scripts, not a framework you will be
defending in two years.

Notice the shape of what survives. Two are infrastructure. The third,
judgment, is not a job a model gets promoted into -- it is the job.
-->

---

<!-- _class: lead -->

# How do you 10x again?

## <span class="tenx">You don't. You manage.</span>

---

# Rung 10: the moves that cleared every rung

<div class="figsplit">
<div>

- **Diversify** — MCP servers, context, skills
- **Requirements first**, then shard
- **Isolate** — one worktree, one brief, one job
- **Delegate specifics**, with a check it can run
- **Keep swarms under five**

**Not agent techniques. The job description.**

</div>
<div class="figure">

<svg viewBox="0 0 220 400" width="160" role="img" aria-label="A ceiling-mounted artificial intelligence with a single glowing yellow optic.">
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

<div class="cap">An orchestrator with<br>nobody above it.</div>

</div>
</div>

<!--
Every rung was a management problem wearing an engineering hat.

Diversify: a team of clones is one agent with a bigger bill.

Requirements first: an agent handed a new spec mid-task pays what a
person pays mid-sprint. Write the requirements and the architecture
down, then shard.

Isolate: context switching drains agents too, they just do not complain
about it.

Delegate specifics: not "help with the cache" -- a scoped task, a check
it can run, and a definition of done.

Under five: span of control transfers, but only as a context limit.
Careers, politics and accountability do not transfer. Take the org
chart's shape, not its rationale.
-->

---

# The shape that scales

```text
You
└── Lead                single decision point
    ├── Researcher      read-only, no spawn tool
    │   └── N subagents, one per source
    └── Coder × N       one worktree each
```

- **Fan out at the leaves. Stay singular at the decisions.**
- Never a second lead until the first one is full
- Never give the read-only researcher a spawn tool
- Differentiate researchers by **evidence**, not personality

<!--
Depth two. Parallelism comes from the N's, coordination from the single
lead, isolation from the worktrees and from the researcher's missing
write tools.

Why no second lead: a layer buys context isolation and costs a lossy
summary. A lead with no file tools cannot check a sub-lead's synthesis
against the code.

Why no spawn tool on the researcher: it is read-only so it can safely
ingest untrusted sources. Let it spawn, and injected content becomes a
work order.

Duplicate coders freely -- they do different work. Duplicate researchers
and you pay N times for one answer.

Depth is capped anyway: subagents nest three layers by default, and
agent-team teammates cannot nest at all.
-->

---

# Practices

<div class="columns small">
<div>

- **PR too big?** Decompose, then fan out. One PR per chunk.
- **Worktrees** for anything parallel
- **Share agents across repos** — subtree or plugin, not submodule
- **Review bot before human** — `/code-review` in a fresh subagent

</div>
<div>

- **Auto-update CODEOWNERS** from `git log`. Humans approve.
- **Same prompt twice?** Make it a skill.
- **Ask Claude to write your hooks.** Review the diff like code.
- **Humans review outcomes**, not transcripts

</div>
</div>

<!--
One line each on purpose. Pick the two that match the room and expand
those; do not read the list.

CODEOWNERS: a scheduled routine derives owners per directory and opens a
PR. Humans approve, never type.

Finding repeat work: log spawns and messages, then search your own
transcripts for the same prompt twice. The second time is the signal.
-->

---

# Show, don't tell

- Give every agent something it can **run**
- Tests, an exit code, a screenshot diff, a checklist
- The coder runs them. The researcher scores them. The lead accepts **evidence**.
- Without a check, "looks done" is the only signal
- **And then you are the verification loop again**

<!--
This is rung 3's wall rebuilt by hand, which is why it belongs at the
end: every practice in this deck fails without a machine-checkable
definition of done.

If you want one concrete ask for the audience to take home, make it this
one. It is the cheapest thing on the list and it is the one that decides
whether any of the rest works.
-->

---

# Tying it together

- **The climb.** Every rung was cleared by a management move, not a smarter model.
- **The research.** Solo is already the 10x. Structure contains errors; it cannot fix clones.
- **The wiring.** One config line: 0 → 20 → 93 hops, same answer. Cost, not correctness.
- **The stop rule.** As simple as possible, but no simpler.

<!--
Four beats, one each. If you are over time, this slide can be the last
content slide -- everything after it is the close.
-->

---

# Google already ran this experiment

- **Project Oxygen** set out to show that managers don't matter
- 10,000+ data points: reviews, surveys, interviews
- Found the opposite — better managers, better results, **lower turnover**
- Top behaviours: coach, **empower without micromanaging**, clear vision, results
- **The same list works on agents**

<span class="sources">Google re:Work, *Project Oxygen* — begun 2008; eight behaviours, extended to ten in 2018</span>

<!--
The story is the good part: Google's founders genuinely believed managers
were overhead at best and an obstacle at worst, and they tried to prove it
with their own data. The data said the opposite, and hard enough that the
behaviours became the manager training programme.

The behaviour that matters most for this room is the second one --
empowers the team and does not micromanage. That is the same wall as rung
3: supervise every keystroke and you are the runtime again, whether the
worker is a person or a process.

Worth one line if challenged: this is research about humans, and the claim
here is not that agents have feelings. It is that the practices which
scale a team of people are the practices that scale a fleet of agents,
because both bottleneck on the same thing -- one person's attention.

Check the exact behaviour wording against re:Work before you present; the
list was eight in 2008 and ten from 2018, and the phrasing shifted.
-->

---

# We're all managers now

AI takes the mechanical parts of the job.

What is left is judgment: what to build, what to reject, what "done" means.

**The case for managers is the case for humans, even in the AI age.**

<!--
Pause here. This is the thesis.
-->

---

# <svg class="chili" viewBox="0 0 40 44" width="34" height="37" role="img" aria-label="chili pepper"><title>Spicy</title><path d="M22 31 L9 39 L19 26 Z" fill="#cf2f26"/><path d="M22 15 C30 20 29 29 21 32" fill="none" stroke="#cf2f26" stroke-width="13" stroke-linecap="round"/><path d="M25 19 C28 22 28 26 26 29" fill="none" stroke="#e8756c" stroke-width="2.5" stroke-linecap="round"/><path d="M21 12 C20 7 17 5 13 6" fill="none" stroke="#3f8f3f" stroke-width="3.5" stroke-linecap="round"/><ellipse cx="22" cy="13" rx="6" ry="3.5" fill="#4a9a3f" transform="rotate(-12 22 13)"/></svg> Sorry, not sorry

- Assembly → compilers → libraries → frameworks → agents
- Every layer made the one below it **less scarce**
- **Nobody has ever paid for code.** They pay for what it does for someone.
- Never automated: knowing which problem is worth solving, and for whom

<!--
Deliver this warmly and do not soften the content. The room has spent
forty minutes on tooling; this is the line that says tooling was never
the point.

Each time a layer arrived, the people who defined the job as typing the
layer below had a bad decade. The people who defined it as solving
someone's problem did not.

And if an agent can now do the part you liked most, that says nothing
about your worth -- it says the value moved, the way it has moved every
decade since punch cards.

Do not let it land as "learn to love it". The next slide is the other
half, and it is the one people remember.
-->

---

# A ladder is one shape a career can have

<div class="columns">
<div>

- The deck is a ladder. **Your career doesn't have to be.**
- You choose the rung — including the ground
- Climbing is a **trade**, not a promotion
- Burning out as the hub is **structural**, not personal

</div>
<div>

- **They work for you**, not the other way round
- Async isn't free — watch your hours, not just theirs
- Be a manager you'd want: **no 3am drops, no Friday-night dumps**
- **Micromanaging doesn't scale either** — outcomes, not transcripts
- We need new norms. They're being set by accident.

</div>
</div>

<!--
Slow down here. Say it plainly and do not rush to the close.

The rung point: staying at rung 1 -- one agent, deep craft, small scope
-- is a choice, not a failure to climb. A ladder has one direction; a
career has several, and most of the good ones are sideways.

On the hub: nobody is meant to be five sessions' worth of interrupt
handler. That is a structural problem, not a personal weakness.

On being nicer: how you talk to an agent is practice for how you talk to
people. Clear briefs instead of vague pressure. No work dropped at 3am
or 5pm on Friday just because something is awake to receive it. No
blaming the worker for a spec you never wrote down. Every bad managerial
habit is cheaper to rehearse on an agent -- and rehearsal is exactly
what it is.

Micromanaging is the one that bites twice. Watching every tool call and
re-reading every transcript is both the bad habit and a hard scaling
limit: it puts you back in the wheel from rung 3. You cannot supervise
ten agents keystroke by keystroke any more than you can supervise ten
people that way. Ask for evidence, read the outcome, and let the middle
be theirs.

On the norms: when work never blocks on you, what is a sane week?
On-call for agents. Review load when diffs arrive faster than anyone can
read them. How much output is "enough". Those are being decided right
now, mostly by default, and we will have to reconsider them on purpose
-- as teams and as an industry.

If it fits your setting, say the personal version out loud: which rung
you actually work at, and what climbing cost you.
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
<div class="caption">The cake is a lie.</div>

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
-->---

# Sources

<div class="sources">

- Kim et al., *[Towards a Science of Scaling Agent Systems](https://arxiv.org/abs/2512.08296)*, arXiv 2512.08296, Dec 2025. [Google Research blog](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/)
- Google re:Work, *[Project Oxygen / the research behind great managers](https://rework.withgoogle.com/guides/managers-identify-what-makes-a-great-manager/)*. See also Garvin, *[How Google Sold Its Engineers on Management](https://hbr.org/2013/12/how-google-sold-its-engineers-on-management)*, HBR, Dec 2013
- Anthropic Frontier Red Team, *[Patterns and problems in emerging multiagent systems](https://www.anthropic.com/research/multiagent-systems)*, Aug 2026
- Brooks, *[The Mythical Man-Month](https://en.wikipedia.org/wiki/The_Mythical_Man-Month)*, 1975. Conway, *[How Do Committees Invent?](https://www.melconway.com/Home/Committees_Paper.html)*, 1968. Sutton, *[The Bitter Lesson](http://www.incompleteideas.net/IncIdeas/BitterLesson.html)*, 2019
- "As simple as possible, but no simpler": widely attributed to Einstein, [a paraphrase](https://quoteinvestigator.com/2011/05/13/einstein-simple/) of his 1933 Herbert Spencer lecture
- BMAD-METHOD: [github.com/bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) &middot; [issue #2211](https://github.com/bmad-code-org/BMAD-METHOD/issues/2211) &middot; [BAD](https://github.com/stephenleo/bmad-autonomous-development)
- Claude Code docs: [sub-agents](https://code.claude.com/docs/en/sub-agents), [agent-teams](https://code.claude.com/docs/en/agent-teams), [cross-session-messaging](https://code.claude.com/docs/en/cross-session-messaging), [worktrees](https://code.claude.com/docs/en/worktrees), [agents in parallel](https://code.claude.com/docs/en/agents), [hooks](https://code.claude.com/docs/en/hooks), [skills](https://code.claude.com/docs/en/skills)

</div>
