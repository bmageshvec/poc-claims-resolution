# Dispute Claims Resolution — Architecture Workspace

Target-state architecture for migrating **Pega OOTB Smart Dispute** to a **domain-driven microservices platform on AWS**, covering card and e-commerce disputes over **MCOM (Mastercard)** and **VROL (Visa)**.

## Folder structure

```
dispute-architecture/
├── README.md                                  ← you are here
├── docs/
│   └── dispute-claims-resolution-architecture.md   ← the main architecture document
├── diagrams/
│   ├── C4_ContextClaimsResoluion.drawio.png        ← original C4 L1 context (source input)
│   └── mermaid/                                    ← 18 diagrams, extracted for reuse
└── source/
    └── C4_ContextClaimsResoluion.drawio            ← editable draw.io source
```

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

## Diagram index (`diagrams/mermaid/`)

| File | Type | Shows |
|---|---|---|
| `01-pega-case-type-hierarchy` | graph | Pega OOTB case-type tree (as-is) |
| `02-pega-coupling-hotspots` | graph | Why the monolith resists change |
| `03-ddd-subdomain-classification` | graph | Core / Supporting / Generic subdomains |
| `04-context-map` | graph | **The context map with integration patterns** |
| `05-bin-scheme-resolution-sequence` | sequence | **BIN → VROL/MCOM resolution, end to end** |
| `06-network-router-strategy-class-model` | class | Adapter/strategy pattern for scheme routing |
| `07-canonical-event-state-machine` | state | Published-language event lifecycle |
| `08-c4-l1-system-context` | graph | C4 L1 (elaborates the supplied draw.io context) |
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

All 18 diagrams validated against the Mermaid parser — 0 failures.

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
