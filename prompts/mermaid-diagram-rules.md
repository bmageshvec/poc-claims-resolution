# Mermaid Diagram Ruleset — reusable prompt

**What this is.** A model-agnostic prompt you paste in front of any request for a Mermaid diagram. It encodes the rules that keep diagrams parseable, readable, and honest about what Mermaid can and cannot do.

**How to use it.** Paste everything from *"BEGIN PROMPT"* to *"END PROMPT"*, then add your request underneath. Works with any LLM.

> **Every syntax claim in §6 and §7 was verified against Mermaid 10.9.8** by parsing test cases, not assumed. Where behaviour is version-sensitive it is marked.

---

## BEGIN PROMPT

You are producing a Mermaid diagram. Follow these rules. If a rule conflicts with what I asked for, tell me rather than silently breaking it.

---

### 1 · Pick the right diagram type first

Choose by **what the reader needs to understand**, not by what's easiest to draw.

| The reader needs to know | Type | Why this one |
|---|---|---|
| What state is a thing in, which transitions are legal, which states are terminal | `stateDiagram-v2` | Only type with native semantics for "in exactly one state at a time" and terminal states |
| Who talks to whom, in what order, over elapsed time | `sequenceDiagram` | Participants + ordered messages + a time axis. Cannot express loops or terminal states |
| A decision procedure with branches and exits | `flowchart` | Nodes are *activities and gateways*, not states |
| Structure: boxes and how they connect | `flowchart` | Default choice for architecture and system maps |
| Tables, keys, cardinality | `erDiagram` | Crow's-foot notation is built in |
| Classes, interfaces, inheritance | `classDiagram` | — |
| Work over calendar time | `gantt` | — |

**The distinction people get wrong:** a flowchart's boxes are *things that happen*; a state diagram's boxes are *places the subject rests*. "Awaiting Response" is a state something sits in for 45 days — a flowchart has no way to say that. If you catch yourself drawing a lifecycle as a flowchart, stop and use `stateDiagram-v2`.

---

### 2 · One concern per diagram

- **Maximum ~15 nodes.** Beyond that, split into an overview plus detail diagrams.
- **Maximum 2 levels of abstraction.** Don't mix "System A" with "the retry loop inside System A".
- If a diagram needs a paragraph of prose to be understood, it is doing too much. Split it.
- Detail belongs in a **table beside the diagram**, not inside the boxes.

---

### 3 · Labels

- **Node labels: ≤ 6 words.** Longer detail goes in an adjacent table.
- Use `<br/>` for deliberate line breaks. Never rely on auto-wrap.
- **No `<b>` or `<i>`** — see §6 rule 9. For emphasis, put the key text on its **first line** or use CAPITALS. Structure carries emphasis; markup does not.
- Put the **type** on its own line when it aids reading: `Name<br/>[External System]<br/>short description`.
- Every edge that isn't self-evident gets a label. Every edge in an `erDiagram` **must** have one — it's a syntax requirement.
- Edge labels: ≤ 8 words. If longer, number the edge and explain in a table.

---

### 4 · Layout — work with the renderer, not against it

**Mermaid auto-layouts. You do not control node positions.** Accept this; do not fight it.

- Set direction explicitly: `flowchart TB` (hierarchy, process) or `flowchart LR` (pipeline, timeline). `LR` fits wide screens; `TB` fits documents.
- **Declaration order affects layout.** Declare nodes in the order you want them ranked.
- Use `subgraph` to cluster, and set `direction` inside each one — this is supported and works.
- Bundle edges: many edges into one node makes a hairball. Introduce an intermediate node instead.
- To force ranking without drawing a line, use an **invisible link**: `A ~~~ B`.

If you need pixel-exact positioning, fixed swimlanes, or precise connection points — **say so and recommend draw.io or hand-authored SVG instead**. Do not pretend Mermaid can do it.

---

### 5 · The connection-point problem, and how to work around it

**The limitation:** Mermaid has no port or anchor control. Every edge touching a node enters at a renderer-chosen point, so multiple edges *merge visually* at the same anchor and become impossible to trace. There is no `exitX`/`entryY` as in draw.io.

**Do not try to fix this with layout.** Fix it by making each edge *individually identifiable*. Use these four tools, in this order of preference:

**5.1 — Line style carries meaning.** All of these parse:

| Syntax | Renders as | Reserve it for |
|---|---|---|
| `A --> B` | solid arrow | Primary / synchronous / default flow |
| `A -.-> B` | dotted arrow | Secondary, asynchronous, optional, or an unenforced reference |
| `A ==> B` | thick arrow | High-volume, system-to-system, or the critical path |
| `A --- B` | solid, no arrow | Association without direction |
| `A -.- B` | dotted, no arrow | Weak or informational association |
| `A === B` | thick, no arrow | Strong undirected association |
| `A --x B` | arrow with cross | Blocked, rejected, terminated |
| `A --o B` | arrow with circle | Aggregation, composition |
| `A <--> B` | bidirectional | Two-way exchange |
| `A ~~~ B` | **invisible** | Layout hint only — forces rank, draws nothing |

**5.2 — Colour the edges by category.** `linkStyle` takes a **zero-based index in declaration order**:

```
linkStyle default stroke:#8C99A6,stroke-width:1.5px
linkStyle 0,1,2 stroke:#0D6EFD,stroke-width:2px
linkStyle 3     stroke:#D1495B,stroke-width:2px,stroke-dasharray:6 4
```

> **Fragile:** indices shift if you insert an edge. Always set `linkStyle default` first, then override the few that matter, and add a `%%` comment naming what each index is.

**5.3 — Colour the nodes by kind** with `classDef` + `class`:

```
classDef actor   fill:#0D3B66,color:#FFFFFF,stroke:#092845,stroke-width:2px
classDef inScope fill:#1061B0,color:#FFFFFF,stroke:#0A3D6B,stroke-width:4px
classDef ext     fill:#8C8C8C,color:#FFFFFF,stroke:#6C6C6C,stroke-width:2px
class A,B actor
class C inScope
class D,E ext
```

**5.4 — Split the diagram.** If three edges still can't be told apart, the diagram is overloaded. Split it.

**Always add a legend** when line style or colour carries meaning — as a table beside the diagram, not as a node inside it.

---

### 6 · Escaping and syntax — verified failure modes

These are the ways Mermaid actually breaks. **Verified on 10.9.8.**

| # | Rule | Breaks | Works |
|---|---|---|---|
| 1 | **Quote any label containing `()`** | `A[Node (x)]` | `A["Node (x)"]` |
| 2 | **Quote edge labels containing `()`** | `A -->\|label (x)\| B` | `A -->\|"label (x)"\| B` |
| 3 | **ER entity names need ≥ 2 characters** — a single-character name on the *target* side fails | `T \|\|--o{ U : x` | `TT \|\|--o{ UU : x` |
| 4 | **ER attribute types must be a single token** | `varchar(255) id PK` | `varchar id PK "255 chars"` |
| 5 | **`erDiagram` does not support `classDef`** — no styling at all | `classDef x fill:#f00` inside `erDiagram` | Convey grouping through **naming conventions** and an external legend |
| 6 | **`sequenceDiagram` does not support `classDef`** | `classDef` in a sequence diagram | Use `box <colour> <name> … end` to group participants |
| 7 | **Every `erDiagram` relationship needs a label** | `A \|\|--o{ B` | `A \|\|--o{ B : "has"` |
| 8 | Use HTML entities for reserved characters | a bare `#` | `#35;` · `#quot;` for `"` |
| 9 | **Do not use `<b>` or `<i>` for emphasis.** They *parse* fine but only render where `htmlLabels` is enabled — on GitHub, in many Confluence versions and in draw.io's Mermaid import they appear **literally as `<b>…</b>`** | `A["<b>Name</b><br/>detail"]` | `A["Name<br/>detail"]` — put the emphasised text on its own first line, or use CAPITALS |

> **Rule 9 is the one that bites in review.** Parsing is not rendering. `mermaid.parse()` accepts these tags happily; the reader then sees raw markup in the box. Only `<br/>` is portable — it is required for line breaks and is honoured everywhere.

**These are safe** — all verified to parse **and** render portably:

- `&`, `·`, `—`, `≤`, `→` and other Unicode, both bare and quoted
- **`<br/>`** inside quoted labels — the only HTML tag you should use
- `<<interface>>`, `<<abstract>>` stereotypes in `classDiagram` — these are Mermaid syntax, not HTML
- Commas, colons and semicolons inside quoted labels
- `%%` comment lines
- `%%{init: {'flowchart': {'curve': 'linear'}} }%%` config directives, as the **first line**
- `direction LR` / `direction TB` inside a `subgraph`
- `note right of X : text` and composite `state X { … }` in `stateDiagram-v2`
- `autonumber` and `box rgb(200,220,240) Name … end` in `sequenceDiagram`
- Markdown strings: `` A["`**bold**`"] ``

---

### 7 · Per-type rules

**`flowchart`**
- Declare direction on line 1. Quote every label. Use `subgraph … end` with an explicit `direction`.
- Node shapes carry meaning — be consistent: `[]` process · `{}` decision · `([])` start/end · `[()]` datastore · `[[]]` subroutine.

**`sequenceDiagram`**
- `autonumber` on, always — it gives the reader something to cite.
- Use `Note over A,B:` for context, `alt` / `opt` / `loop` for branches.
- **Cap `alt` blocks at 2–3.** More than that means the wrong diagram type.
- Group participants with `box`.

**`stateDiagram-v2`**
- Set `direction TB` or `LR` explicitly.
- Label every transition with its **guard** — the condition that fires it.
- Show terminal states with `[*]`. If nothing is terminal, question whether it's really a state machine.
- Nest with `state Name { … }` for composite states.

**`erDiagram`**
- Crow's foot: `|o` zero-or-one · `||` exactly-one · `}o` zero-or-more · `}|` one-or-more. Braces point **away** from the entity they describe.
- Line style: `--` identifying (child cannot exist alone) · `..` non-identifying (independent).
- Read `A ||--o{ B` as: *one A has zero or more B; each B belongs to exactly one A.*
- Entity names ≥ 2 characters. Types as single tokens. Every relationship labelled.
- **No styling is possible** — carry grouping in names, explain it in a legend table.

---

### 8 · Default palette

Use these unless the domain dictates otherwise. Consistency across a set of diagrams matters more than any individual choice.

| Role | Fill | Stroke | Text |
|---|---|---|---|
| Person / actor | `#0D3B66` | `#092845` | `#FFFFFF` |
| **In scope** (the subject) | `#1061B0` | `#0A3D6B`, width 4 | `#FFFFFF` |
| Owned, supporting | `#2A9D8F` | `#1D7A6F` | `#FFFFFF` |
| External system | `#8C8C8C` | `#6C6C6C` | `#FFFFFF` |
| Warning / risk / blocked | `#D1495B` | `#9D2235` | `#FFFFFF` |
| Data store | `#E9C46A` | `#C9971A` | `#1A2733` |
| Neutral edge | — | `#54606C` | — |

Rules: **the in-scope element gets the heaviest stroke**, nothing else. Maximum **five** fills per diagram. If colour encodes meaning, a legend is mandatory. Never use colour as the *only* signal — pair it with line style or shape, for accessibility and for greyscale printing.

When a diagram involves a recognisable brand, use its real colours — it removes a whole class of ambiguity.

---

### 9 · Before you output — self-check

Do not return a diagram until all of these hold:

- [ ] The type matches what the reader needs (§1)
- [ ] ≤ 15 nodes, one concern, ≤ 2 abstraction levels
- [ ] Every label with `()` is quoted
- [ ] Every `erDiagram` relationship has a label; every entity name is ≥ 2 characters
- [ ] No `classDef` inside `erDiagram` or `sequenceDiagram`
- [ ] **No `<b>` or `<i>` anywhere** — only `<br/>`
- [ ] Direction is explicit
- [ ] A legend exists if line style or colour carries meaning
- [ ] No edge crosses a node where a different route was available
- [ ] It renders — you have mentally traced every edge to a distinguishable endpoint

**State your confidence.** If you cannot verify it parses, say so explicitly: *"Not parser-verified — validate at mermaid.live before use."*

---

### 10 · Output format

Return, in this order:

1. **One line** stating the diagram type and why it was chosen.
2. The diagram in a fenced ` ```mermaid ` block — nothing else inside the fence.
3. A **legend table** if colour or line style carries meaning.
4. A **detail table** for anything too long to sit in a node.
5. Any **assumptions** you made, and anything Mermaid could not express that would need draw.io or SVG.

Do not narrate the diagram in prose. If it needs narrating, redraw it.

## END PROMPT

---

## Appendix A — Copy-paste invocation template

```
[paste BEGIN PROMPT … END PROMPT above]

Now draw: <what>

Audience:            <exec / architect / engineer / auditor>
Purpose:             <the one question this must answer>
Must show:           <non-negotiables>
Must NOT show:       <out of scope>
Direction:           <TB | LR | your call>
Brand colours:       <if any>
Parser-verified:     <yes — I will validate | no — best effort>
```

## Appendix B — Validating before you ship

Mermaid's own parser is the only reliable check. Rendering in a preview pane is not — some errors only surface at parse time.

```bash
npm install mermaid@10 jsdom
```

```javascript
// validate.mjs — node validate.mjs file.mmd [more.mmd ...]
import fs from 'fs';
import { JSDOM } from 'jsdom';
const dom = new JSDOM('<!DOCTYPE html><body></body>', { pretendToBeVisual: true });
global.window = dom.window;
global.document = dom.window.document;
global.HTMLElement = dom.window.HTMLElement;
global.SVGElement = dom.window.SVGElement;
global.DOMPurify = { sanitize: s => s, addHook: () => {}, setConfig: () => {} };

const mermaid = (await import('mermaid')).default;
mermaid.initialize({ startOnLoad: false, securityLevel: 'loose' });

let failed = 0;
for (const f of process.argv.slice(2)) {
  try {
    await mermaid.parse(fs.readFileSync(f, 'utf8'));
    console.log(`OK   ${f}`);
  } catch (e) {
    failed++;
    console.log(`FAIL ${f}\n     ${String(e.message || e).split('\n')[0]}`);
  }
}
process.exit(failed ? 1 : 0);
```

To validate blocks embedded in markdown, extract them first:

```javascript
const blocks = [...md.matchAll(/```mermaid\n([\s\S]*?)```/g)].map(m => m[1]);
```

> **If you keep extracted `.mmd` files alongside embedded copies, they will drift.** Diff them in CI, or generate one from the other.

## Appendix C — When Mermaid is the wrong tool

Switch to **draw.io** or hand-authored **SVG** when you need any of:

| Requirement | Why Mermaid can't |
|---|---|
| Exact node positions | Auto-layout only |
| Fixed swimlanes or banded layouts | No lane primitive; subgraphs are laid out by connectivity |
| Specific connection points on a node | No port control |
| Guaranteed non-overlapping edge routing | No manual waypoints |
| Custom shapes — C4 person, cylinder variants, icons | Fixed shape set |
| Precise print or slide dimensions | Renderer decides the canvas |

**The honest rule:** Mermaid is for diagrams that live in version control next to the code and change often. draw.io and SVG are for diagrams that go in front of stakeholders and must look exactly one way. Use both — just don't ask either to be the other.
