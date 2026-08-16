# Dispute Claims Resolution — Architecture Workspace

Target-state architecture for migrating **Pega OOTB Smart Dispute** to a **domain-driven, capability-based platform**, covering card and e-commerce disputes over **Mastercard** (MCOM) and **Visa** (VROL).

The solution architecture is **technology-agnostic**: capabilities and qualities are described in Parts 0–11, and products are named only in Part 12, which is expected to be replaced to match your platform standards.

## Folder structure

```
dispute-architecture/
├── README.md                                  ← you are here
├── docs/
│   ├── dispute-claims-resolution-architecture.md   ← the main architecture document (TO-BE)
│   ├── dispute-process-stages.md                   ← the process, stage by stage
│   ├── pega-lite-db-schema.md                      ← Pega Smart Dispute AS-IS DB schema + ERDs
│   └── scheme-lifecycles-and-customer-journeys.md  ← VCR/MDR lifecycles + 4 worked journeys
├── prompts/
│   └── mermaid-diagram-rules.md                    ← reusable ruleset for generating any Mermaid diagram
├── diagrams/                                       ← grouped by owning document
│   ├── C4_ContextClaimsResoluion.drawio.png        ← original C4 L1 context (source input)
│   ├── C4_L1_SystemContext_DisputePlatform.svg     ← ★ presentation master, rendered
│   ├── dispute-e2e-swimlane.svg                    ← ★★ THE end-to-end flow — 8 lanes × 5 phases, one canvas
│   ├── dispute-journey-capture-to-recover.svg      ← ★ the same journey collapsed to 5 phases × 3 lanes
│   ├── phase-detail/                               ←  5 .svg — one per phase, sub-stage level
│   ├── architecture/                               ← 16 .mmd — from the TO-BE architecture doc
│   ├── ERD/                                        ←  4 .mmd — from the AS-IS schema doc
│   ├── lifecycle-journeys/                         ←  8 .mmd — from the lifecycles doc
│   └── pega-product-flow/                          ←  3 .mmd — from the Pega product-flow doc
└── source/
    ├── C4_L1_SystemContext_DisputePlatform.drawio  ← ★ presentation master, editable
    └── dispute-e2e-swimlane.py                     ← regenerates the E2E swimlane (auto-routes, 0 crossings)
```

**Presentation masters vs inline diagrams.** Where a diagram must look exactly one way — the C4 L1 system context — the authoritative artifact is the **draw.io / SVG** pair marked ★. Mermaid cannot hold fixed bands, lane positions or connection points, so the `.mmd` copy in the doc is an approximation. Everything else is Mermaid-first.

## Documents

| Doc | Covers |
|---|---|
| [**`docs/dispute-claims-resolution-architecture.md` §0**](docs/dispute-claims-resolution-architecture.md#0-terminology--read-this-first) | **START HERE — shared glossary.** Scheme vs platform vs programme (VISA/VROL/VCR, MASTERCARD/MCOM/MDR), parties, lifecycle vocabulary, per-scheme terms, DDD terms, and the words that mean two different things depending on the scheme |
| [`docs/dispute-claims-resolution-architecture.md`](docs/dispute-claims-resolution-architecture.md) | **TO-BE — target solution architecture.** Technology-agnostic in Parts 0–11: 17 bounded contexts incl. the new **Reconciliation & Assurance**, a capability catalog, C4 L1–L3, and **the four scheme integration flows** (file / poll / fan-out / reconcile). Products are named only in Part 12 |
| [`docs/pega-lite-db-schema.md`](docs/pega-lite-db-schema.md) | **AS-IS** — the Pega Smart Dispute "lite" physical DB schema (~35 tables), Mermaid ERD legend, 4 ERDs, MCOM/VROL integration tables, table→bounded-context migration map |
| [`docs/dispute-process-stages.md`](docs/dispute-process-stages.md) | **PROCESS** — opens with the **E2E swimlane**: 8 lanes × 5 phases on one canvas, every decision and every integration in a single continuous flow. Then the same journey collapsed to 5 phases × 3 lanes, five zoom-ins at sub-stage level, and the process in stage / path / step table format: intake channels, ingestion & triage, deflection, provisional credit, the scheme cycles, arbitration, appeal, and the parallel compliance / good-faith / recall flows. The operational companion to the architecture |
| [`docs/pega-smart-dispute-product-flow.md`](docs/pega-smart-dispute-product-flow.md) | **AS-IS PRODUCT** — the dispute flow as *Pega* documents it (Smart Dispute Agentic Automation 24.2, Pega Academy): Visa classification, early resolution, the Allocation and Collaboration flows, pre-compliance/compliance, good faith, recall & withdraw. Independently confirms the pre-arbitration filer, and surfaces 7 gaps in our model incl. **appeal** and **fund position** |
| [`docs/scheme-lifecycles-and-customer-journeys.md`](docs/scheme-lifecycles-and-customer-journeys.md) | **SCHEME BEHAVIOUR** — an at-a-glance two-path view, a generalized 6-stage lifecycle, Visa VCR (4 stages / 3 in Allocation) and Mastercard MDR (4 cycles), then one worked example ($249.99 goods-not-received) through both schemes, happy and negative paths. Validated against [Visa's VCR merchant guide](https://usa.visa.com/dam/VCOM/download/merchants/visa-claims-resolution-efficient-dispute-processing-for-merchants-VBS-14.APR.16.pdf), [Mastercom's Dispute Resolution Cycle](https://developer.mastercard.com/mastercom/documentation/dispute-resolution-cycle/) and [Rivero](https://rivero.tech/blog/dispute-lifecycle-explained) |

## Main document — section index

| Part | Section | Answers |
|---|---|---|
| **0** | **Terminology** | Scheme vs platform vs programme; the terms that mean two different things |
| 1 | Executive summary & decisions | **D1–D15**, incl. the five new ones on inbound integrity, reconciliation, ACL boundary, filing party and cycle vocabulary |
| 2 | AS-IS — Pega Smart Dispute | Case types, stages, data model, coupling hot-spots |
| 3 | Domain model | **17 bounded contexts** incl. the new BC-17 Reconciliation & Assurance |
| 4 | Context map | R1–R17 with pattern and justification; rejected patterns |
| 5 | Scheme resolution | Backend, and the exact resolution algorithm |
| 6 | Capability catalog | 22 capabilities by store **class**, not product; granularity rationale; canonical events |
| 7 | C4 model | L1 system context, L2 containers, L3 inside a scheme adapter |
| **8** | **Scheme integration — the four flows** | **FILE · POLL · FAN-OUT · RECONCILE**, their failure modes and required properties |
| **9** | **Reconciliation & assurance** | Why it is a separate context, 8 discrepancy classes, the never-mutate invariant, coverage metrics |
| 10 | Personas, journeys & partner access | Who actually uses the platform; access matrix; three worked journeys |
| 11 | Cross-cutting & NFRs | PCI scope containment, NFR targets, consistency model |
| **12** | **Technology realisation** | **The only section naming products.** Store classes, platform capabilities, runtime, and the one trade-off to decide consciously |
| 13 | Migration roadmap | Phases, coexistence rules, exit criteria |
| 14 | Decision log | ADR-001 … ADR-019, plus seven open questions |

## Diagram index

Diagrams are grouped by the document that embeds them.

### `diagrams/architecture/` — 16, from the TO-BE architecture doc

| File | Type | Shows |
|---|---|---|
| `01-pega-case-type-hierarchy` | graph | Pega OOTB case-type tree (as-is) |
| `02-pega-coupling-hotspots` | graph | Why the monolith resists change |
| `03-ddd-subdomain-classification` | graph | Core / Supporting / Generic subdomains |
| `04-context-map` | graph | **The context map with integration patterns** |
| `05-scheme-resolution-sequence` | sequence | **BIN → scheme resolution, end to end** |
| `06-scheme-adapter-strategy-class-model` | class | Adapter/strategy pattern for scheme routing |
| `07-canonical-event-state-machine` | state | Published-language event lifecycle |
| `08-c4-l1-system-context` | flowchart | **C4 L1** — Issuer POV. The scheme is the only channel to the acquirer, who runs their own dispute system |
| `09-c4-l2-containers` | graph | C4 L2 containers inside "Claims" |
| `10-c4-l3-scheme-adapter` | flowchart | C4 L3 — inside a scheme adapter: Filer, Poller, Journal, two ACLs |
| `11-scheme-integration-four-flows` | flowchart | **The four flows** — file, poll, fan-out, reconcile |
| `12-journey-1-customer-raises-dispute` | sequence | Customer persona, happy path |
| `13-journey-2-partner-response` | sequence | Acquirer response — scheme path and optional partner path |
| `14-journey-3-issuer-adjudication` | sequence | Issuer persona, back-office |
| `15-pci-scope-containment` | flowchart | What is in / out of the cardholder data environment |
| `16-migration-roadmap` | flowchart | Strangler-fig phases |

### `diagrams/ERD/` — 4, from the AS-IS Pega schema doc

| File | Type | Shows |
|---|---|---|
| `01-pega-lite-erd-master` | erDiagram | All ~35 tables, entities only — the navigation page |
| `02-pega-lite-erd-case-core` | erDiagram | Dispute cases, party, card, transaction, reason codes, time bars |
| `03-pega-lite-erd-network-mcom-vrol` | erDiagram | **MCOM & VROL correlation, messages, documents, rulings** |
| `04-pega-lite-erd-platform-rules` | erDiagram | Assignments, history, SLA queue, locks, PegaRULES |

### `diagrams/lifecycle-journeys/` — 8, from the lifecycles & journeys doc

| File | Type | Shows |
|---|---|---|
| `00-at-a-glance-two-visa-paths` | flowchart | **Start here** — Allocation (3 stages, acquirer files) vs Collaboration (4 stages, issuer files) vs MDR |
| `01-generalized-dispute-lifecycle` | flowchart | Both schemes in one picture — 6 stages, exits, compliance side-flow |
| `02-visa-vcr-lifecycle` | state | **Visa VCR** — full state machine, both workflows |
| `03-mastercard-mdr-lifecycle` | state | **Mastercard MDR — 4 cycles**, single evidence-driven flow |
| `04-journey-a-visa-happy-path` | sequence | Merchant can't prove delivery — resolved at stage 2, day 62 |
| `05-journey-b-visa-negative-path` | sequence | CE3.0 evidence → all 4 stages → issuer loses, day 111 |
| `06-journey-c-mastercard-happy-path` | sequence | Same case on MDR — 21 days slower, day 83 |
| `07-journey-d-mastercard-negative-path` | sequence | All 4 cycles → issuer loses, day 134, Reg E 90d breached by 24 |

### `diagrams/pega-product-flow/` — 3, from the Pega product-flow doc

| File | Type | Shows |
|---|---|---|
| `01-pega-visa-allocation-flow` | flowchart | Pega's Allocation flow — **acquirer** files pre-arb; funds stay with issuer |
| `02-pega-visa-collaboration-flow` | flowchart | Pega's Collaboration flow — **issuer** files pre-arb; funds return to acquirer on decline |
| `03-pega-precompliance-compliance-flow` | flowchart | Independent compliance route; 30-day silence = full liability |

### `diagrams/phase-detail/` — 5 SVG, zoom-ins on one column each of the E2E swimlane

These are **magnifications of `dispute-e2e-swimlane.svg`, not separate processes** — same lanes, same colours, more room for sub-stages and exit paths. Three lanes — **issuer systems** (left) · **platform flow and decisions** (centre) · **external platforms** (right) — with one shared line-style key across all five: **grey solid** = internal flow · **blue solid** = synchronous call · **orange dotted** = poll · **purple dashed** = asynchronous / event.

| File | Phase | Decisions and integrations at sub-stage level |
|---|---|---|
| `phase-1-capture.svg` | 1 · Capture | Channel intake → identity & entitlement → core-platform txn lookup → duplicate check → Reg E clock start. Sync to card auth/posting and customer master |
| `phase-2-auto-resolve.svg` | 2 · Auto-resolve & triage | Eligibility rules, reason-code derivation, credit/no-credit decision, straight-through resolve vs route to analyst. Sync to fraud/scoring and GL posting |
| `phase-3-pre-dispute.svg` | 3 · Pre-dispute | **Ethoca alert** and **RDR/Verifi** deflection async-out with poll-back; VROL Merchant Purchase Inquiry and MCOM Collaboration request; merchant-refund vs proceed-to-file decision |
| `phase-4-dispute.svg` | 4 · Dispute (file) | Evidence pack assembly → scheme routing (VROL vs MCOM) → **synchronous file** → poll for acquirer response → represent / accept branch |
| `phase-5-recover.svg` | 5 · Recover | **Who files pre-arbitration?** (Visa Allocation = acquirer; Collaboration & MDR = issuer) → arbitration → appeal ≥ USD 5,000 → settlement write-back, plus the independent reconciliation poll |

All 31 Mermaid diagrams validated against the parser — 0 failures; all 7 SVGs well-formed with 0 box overlaps. All dates, day-counts and scheme response windows in the journeys verified programmatically.

## Which diagram type for which job

| Need to show | Use | Why |
|---|---|---|
| **A lifecycle** — what state is the case in, what transitions are legal, which states are terminal | `stateDiagram-v2` | A lifecycle *is* a state machine. Only this type has native semantics for "currently in exactly one state" and terminal states. |
| **A journey** — who talks to whom, in what order, over elapsed time | `sequenceDiagram` | Participants + ordered messages + time axis. Cannot express loops or terminal states. |
| **A decision procedure** — if X then Y, with exits | `flowchart` | Nodes are *activities and gateways*, not states. Best for eligibility, routing, and cross-scheme overviews with exit points. |
| **Structure** — tables, services, contexts | `erDiagram` / `graph` | — |

## Authoring new diagrams

Use [`prompts/mermaid-diagram-rules.md`](prompts/mermaid-diagram-rules.md) — a model-agnostic ruleset covering diagram-type selection, the connection-point limitation and its workarounds, verified Mermaid syntax gotchas, the shared palette, and a validation script. Every syntax claim in it was verified against Mermaid 10.9.8 rather than assumed.

The palette and line-style key those diagrams follow is [architecture §0.11](docs/dispute-claims-resolution-architecture.md#011-diagram-conventions--the-shared-legend) — one shared legend, not repeated per diagram.

## Pega table naming, in one line

`pc_` = your application data (migrates) · `pr_` = Pega platform machinery (does not) · `pr4_` = PegaRULES, separate schema. Column prefixes: `px` engine-owned read-only, `py` application-writable, `pz` engine-internal. Full decoder in [`docs/pega-lite-db-schema.md` §0](docs/pega-lite-db-schema.md#0-naming-conventions--read-this-first).

## How to use the `.mmd` files

- Paste into <https://mermaid.live> to render or export SVG/PNG.
- draw.io: **Arrange → Insert → Advanced → Mermaid**.
- Confluence / GitHub / GitLab render Mermaid natively in fenced ` ```mermaid ` blocks.

## Open questions before build

1. Issuer-side only, or does the platform also serve the **acquiring** side?
2. Does an existing PCI token vault expose an **account-range dereference** API?
3. Core banking posting API — **synchronous or batch**? (changes the Reg E provisional-credit design)
4. Any **co-badged domestic schemes** in scope?
5. Are **deflection feeds** (Ethoca / Verifi / RDR) already contracted?
6. Single issuing entity or **multi-entity / multi-BIN** tenancy?
