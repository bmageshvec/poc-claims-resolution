# Dispute Claims Resolution — Architecture Workspace

Target-state architecture for migrating **Pega OOTB Smart Dispute** to a **domain-driven microservices platform on AWS**, covering card and e-commerce disputes over **MCOM (Mastercard)** and **VROL (Visa)**.

## Folder structure

```
dispute-architecture/
├── README.md                                  ← you are here
├── docs/
│   ├── dispute-claims-resolution-architecture.md   ← the main architecture document (TO-BE)
│   ├── pega-lite-db-schema.md                      ← Pega Smart Dispute AS-IS DB schema + ERDs
│   └── scheme-lifecycles-and-customer-journeys.md  ← VCR/MDR lifecycles + 4 worked journeys
├── prompts/
│   └── mermaid-diagram-rules.md                    ← reusable ruleset for generating any Mermaid diagram
├── diagrams/                                       ← grouped by owning document
│   ├── C4_ContextClaimsResoluion.drawio.png        ← original C4 L1 context (source input)
│   ├── C4_L1_SystemContext_DisputePlatform.svg     ← ★ presentation master, rendered
│   ├── architecture/                               ← 18 .mmd — from the TO-BE architecture doc
│   ├── ERD/                                        ←  4 .mmd — from the AS-IS schema doc
│   ├── lifecycle-journeys/                         ←  8 .mmd — from the lifecycles doc
│   └── pega-product-flow/                          ←  3 .mmd — from the Pega product-flow doc
└── source/
    └── C4_L1_SystemContext_DisputePlatform.drawio  ← ★ presentation master, editable
```

**Presentation masters vs inline diagrams.** Where a diagram must look exactly one way — the C4 L1 system context — the authoritative artifact is the **draw.io / SVG** pair marked ★. Mermaid cannot hold fixed bands, lane positions or connection points, so the `.mmd` copy in the doc is an approximation. Everything else is Mermaid-first.

## Documents

| Doc | Covers |
|---|---|
| [**`docs/dispute-claims-resolution-architecture.md` §0**](docs/dispute-claims-resolution-architecture.md#0-terminology--read-this-first) | **START HERE — shared glossary.** Scheme vs platform vs programme (VISA/VROL/VCR, MASTERCARD/MCOM/MDR), parties, lifecycle vocabulary, per-scheme terms, DDD terms, and the words that mean two different things depending on the scheme |
| [`docs/dispute-claims-resolution-architecture.md`](docs/dispute-claims-resolution-architecture.md) | **TO-BE** — DDD bounded contexts, 22 microservices, C4 L1–L3, BIN routing decision, AWS deployment, migration roadmap |
| [`docs/pega-lite-db-schema.md`](docs/pega-lite-db-schema.md) | **AS-IS** — the Pega Smart Dispute "lite" physical DB schema (~35 tables), Mermaid ERD legend, 4 ERDs, MCOM/VROL integration tables, table→bounded-context migration map |
| [`docs/pega-smart-dispute-product-flow.md`](docs/pega-smart-dispute-product-flow.md) | **AS-IS PRODUCT** — the dispute flow as *Pega* documents it (Smart Dispute Agentic Automation 24.2, Pega Academy): Visa classification, early resolution, the Allocation and Collaboration flows, pre-compliance/compliance, good faith, recall & withdraw. Independently confirms the pre-arbitration filer, and surfaces 7 gaps in our model incl. **appeal** and **fund position** |
| [`docs/scheme-lifecycles-and-customer-journeys.md`](docs/scheme-lifecycles-and-customer-journeys.md) | **SCHEME BEHAVIOUR** — an at-a-glance two-path view, a generalized 6-stage lifecycle, Visa VCR (4 stages / 3 in Allocation) and Mastercard MDR (4 cycles), then one worked example ($249.99 goods-not-received) through both schemes, happy and negative paths. Validated against [Visa's VCR merchant guide](https://usa.visa.com/dam/VCOM/download/merchants/visa-claims-resolution-efficient-dispute-processing-for-merchants-VBS-14.APR.16.pdf), [Mastercom's Dispute Resolution Cycle](https://developer.mastercard.com/mastercom/documentation/dispute-resolution-cycle/) and [Rivero](https://rivero.tech/blog/dispute-lifecycle-explained) |

## Main document — section index

| § | Section | Answers |
|---|---|---|
| 1 | Executive summary & key decisions | The 10 decisions (D1–D10) that shape everything |
| 2 | Part A — Reverse-engineering Pega Smart Dispute | Case types, stages, data model, coupling hot-spots |
| 3 | Part B — DDD subdomains & bounded contexts | 16 bounded contexts, aggregates, ubiquitous language, invariants |
| 4 | Part C — Context map & integration patterns | R1–R17 relationships with pattern + justification; rejected patterns |
| 5 | **Part D — The BIN routing decision (FE vs BE)** | **Backend. Why, and the exact resolution algorithm** |
| 6 | Part E — Microservice catalog | 22 services: responsibility, datastore, APIs, events; granularity rationale |
| 7 | Part F — C4 model (L1/L2/L3) | System context, containers, components of `dispute-case-svc` and `mcom-adapter-svc` |
| 8 | Part G — Persona journeys & PAI | Customer / Issuer direct; Acquirer / Merchant via PAI; access matrix |
| 9 | Part H — Network integration: MCOM & VROL | Capability comparison, canonical↔scheme mapping, reliability pattern |
| 10 | Part I — AWS deployment architecture | EKS, MSK, Step Functions, Aurora, DynamoDB, PCI subnet isolation |
| 11 | Part J — Cross-cutting & NFRs | PCI scope containment, NFR targets, security, consistency model |
| 12 | Part K — Strangler-fig migration roadmap | 6 phases, coexistence rules, exit criteria |
| 13 | Appendix — Decision log | ADR-001 … ADR-014, incl. rejected options |

## Diagram index

Diagrams are grouped by the document that embeds them.

### `diagrams/architecture/` — 18, from the TO-BE architecture doc

| File | Type | Shows |
|---|---|---|
| `01-pega-case-type-hierarchy` | graph | Pega OOTB case-type tree (as-is) |
| `02-pega-coupling-hotspots` | graph | Why the monolith resists change |
| `03-ddd-subdomain-classification` | graph | Core / Supporting / Generic subdomains |
| `04-context-map` | graph | **The context map with integration patterns** |
| `05-bin-scheme-resolution-sequence` | sequence | **BIN → VROL/MCOM resolution, end to end** |
| `06-network-router-strategy-class-model` | class | Adapter/strategy pattern for scheme routing |
| `07-canonical-event-state-machine` | state | Published-language event lifecycle |
| `08-c4-l1-system-context` | flowchart | **C4 L1** — banded: personas / software systems / other systems. Acquirer & Merchant work the case in the **scheme portals**, not our platform; PAI is a secondary deflection channel |
| `09-c4-l2-containers` | graph | C4 L2 containers inside "Claims" |
| `10-c4-l3-dispute-case-svc` | graph | C4 L3 — the core aggregate service |
| `11-c4-l3-mcom-adapter-acl` | graph | C4 L3 — the anti-corruption layer in detail |
| `12-journey-1-customer-raises-dispute` | sequence | Customer persona, happy path |
| `13-journey-2-partner-pai-response` | sequence | Acquirer & Merchant via PAI (both paths) |
| `14-journey-3-issuer-adjudication` | sequence | Issuer persona, back-office |
| `15-network-reliability-pattern` | graph | Outbox, FIFO, idempotency, time-bar-aware DLQ |
| `16-aws-deployment` | graph | AWS target deployment |
| `17-pci-scope-containment` | graph | What is in / out of the CDE |
| `18-migration-roadmap` | graph | Strangler-fig phases |

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

All 33 diagrams validated against the Mermaid parser — 0 failures. All dates, day-counts and scheme response windows in the journeys verified programmatically.

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
