# Dispute Process — stage by stage

**What this is.** The end-to-end dispute process laid out in the stage / path / step format, documenting everything established across the analysis of the Visa VCR guide, Mastercom's documentation, Pega's product material and the scheme lifecycles.

**Companion documents**

| Doc | Covers |
|---|---|
| [`dispute-claims-resolution-architecture.md`](./dispute-claims-resolution-architecture.md) | Target architecture — bounded contexts, the four scheme integration flows, capability catalog |
| [`scheme-lifecycles-and-customer-journeys.md`](./scheme-lifecycles-and-customer-journeys.md) | The Visa and Mastercard lifecycles with four worked journeys and real dates |
| [`pega-smart-dispute-product-flow.md`](./pega-smart-dispute-product-flow.md) | The AS-IS flow as Pega documents it |
| [`dispute-claims-resolution-architecture.md` §0](./dispute-claims-resolution-architecture.md#0-terminology--read-this-first) | Shared glossary — scheme vs platform vs programme |

> **A note on "Ingestion to Pega".** The stage is *ingestion to the dispute platform*. Today that platform is Pega; in the target it is the Issuer Dispute Resolution Platform. The process is the same either way, so this document names the stage by what it does rather than by the product.

---

## 1. The process at a glance

Blank cells continue the row above, as in a merged spreadsheet cell.

| # | STAGE | PATH | CHANNEL / STEP | Who acts | Outcome |
|---|---|---|---|---|---|
| **1** | **INTAKE** | Customer self-serves digitally | Public website live-sign form | Cardholder | `Complaint` or `Claim` raised |
| | | | Mobile app | Cardholder | `Claim` raised |
| | | Customer contacts the bank | Calls — phone banking | Cardholder → CSR | `Claim` raised on their behalf |
| | | | Live chat | Cardholder → CSR | `Claim` raised on their behalf |
| **2** | **INGESTION & TRIAGE** | Automated where possible, agent on exception | Identity resolution | Platform / BackOffice | `Complaint` promoted to `Claim` |
| | | | Validation | Platform | Claim structurally complete |
| | | | Fraud detection | Fraud platform | Risk score, linked fraud case |
| | | | Duplicate validation | Platform | New · linked · reassertion · duplicate |
| | | | Auto-resolve | Platform | Low-value write-off, merchant credit found |
| **3** | **PRE-DISPUTE / DEFLECTION** *(optional)* | Merchant given a chance to resolve | Scheme deflection programme | Issuer → scheme → merchant | Merchant refunds — **no dispute filed** |
| | | | Merchant enquiry | Issuer → scheme → merchant | Additional data supplied |
| **4** | **PROVISIONAL CREDIT** | Regulatory, independent of the scheme | Credit the cardholder | Issuer | Cardholder made whole |
| **5** | **FIRST CHARGEBACK** *(Mastercard)* **/ DISPUTE** *(Visa)* | Issuer files | Build and file cycle 1 | **Issuer** | Funds move acquirer → issuer |
| **6** | **SECOND PRESENTMENT / REPRESENTMENT** *(Mastercard)* **/ DISPUTE RESPONSE** *(Visa Collaboration)* | Acquirer defends | Accept · partial accept · reject | **Acquirer** | Funds **return to the acquirer** on a decline |
| | | **Not present in Visa Allocation** — the cycle is eliminated | **No Dispute Response stage exists.** The acquirer's only route to challenge is pre-arbitration | — | Stage skipped. **Funds remain with the issuer — no swap** |
| **7** | **PRE-ARBITRATION** | Last bilateral chance to settle | File pre-arbitration | **Varies — see §7** | Accepted, declined, or lapsed |
| **8** | **ARBITRATION** | Scheme decides | File arbitration case | Whoever filed pre-arb | **Binding ruling** + fees |
| **9** | **APPEAL** *(threshold-bound)* | Either party, disputed amount at or above the scheme threshold | File appeal | Issuer or acquirer | **Final** ruling |
| **10** | **RESOLVE & CLOSE** | Book the outcome | Final credit · PC reversal · write-off · recovery · fees | Issuer | Case closed, customer notified |
| **P** | **PARALLEL FLOWS** | Independent of the cycles above | Pre-compliance → compliance | Either party | Ruling on a rule violation |
| | | | Good faith | Issuer | Voluntary payment after the time bar |
| | | | Recall / withdraw | The initiating party | Case withdrawn |

---

## 2. Stage 1 · INTAKE

| Path | Channel | Authenticated? | Produces | Key control |
|---|---|---|---|---|
| **Customer self-serves digitally** | Public website live-sign form | **Often not** | **`Complaint`** | Identity must be resolved before it becomes a claim |
| | Mobile app | Yes | `Claim` | Step-up authentication before submission |
| **Customer contacts the bank** | Phone banking | Yes — CSR verifies on the call | `Claim` | Verification depth appropriate to money movement |
| | Live chat | Yes — session-authenticated | `Claim` | Same as phone |

### 2.1 Why unauthenticated intake produces a Complaint, not a Claim

An unauthenticated form cannot support a dispute case directly:

| Blocked by lack of identity | Consequence |
|---|---|
| Regulatory notice | Cannot establish the notice came from the consumer or an authorised user |
| Deduplication | No account context, so no check against an existing open dispute |
| Scheme resolution | No account → no settlement record → no routing decision |
| Fraud exposure | Anyone knowing a transaction reference could trigger provisional credit on another person's account |
| PCI / PII | An open form collecting card details drags the web tier into scope |

**So Scenario 1 has one more step than Scenario 2** — identity resolution, before the case exists.

> **⚠ A compliance question to settle.** The regulatory clock starts on *notice*, not on identity resolution. If a form arrives Monday and identity is resolved Thursday, three days may already be gone. Compliance should rule on whether `Complaint` is a safe state to linger in, because it changes the SLA on the triage queue.

### 2.2 The document-collection sub-flow

Where evidence is needed from the customer:

| Step | Do | Don't |
|---|---|---|
| Ask for evidence | Only when the **rules capability says this reason code requires it** | Blanket-request documents on every claim |
| Send the request | To the **address on file**, never one supplied on the call | Accept a new contact address at dispute time |
| Receive the document | Tokenised, time-limited **secure upload link** — lands straight on the case | Email attachments into a shared mailbox |
| Attach to the case | Automatic, on upload | Manual download-and-re-upload by an agent |
| If nothing arrives | **Proceed anyway** — the provisional-credit clock does not wait | Block the case pending documents |

> **The document chase and the regulatory clock run in parallel, never in sequence.** Provisional credit is due on its own timetable whether or not the customer replied.

---

## 3. Stage 2 · INGESTION & TRIAGE

| Step | What it does | Where the answer comes from | Outcome if it fails |
|---|---|---|---|
| **Identity resolution** | Match an unauthenticated complaint to a customer and account | Party reference | Discarded — not our customer |
| **Validation** | Claim structurally complete; transaction exists and is disputable | Transaction retrieval | Rejected — transaction not found |
| **Fraud detection** | Risk score and linkage to an existing fraud case | Fraud platform | Proceeds with degraded fallback |
| **Duplicate validation** | New · linked · reassertion · duplicate | Dedup index | Rejected as duplicate |
| **Auto-resolve** | Low-value write-off, or merchant credit already found | Rules capability | Falls through to normal handling |
| **Eligibility** | Is there a right? Which reason code, time bar, evidence, pre-conditions? | Rules capability | Denied — no right, or time bar expired |
| **Scheme resolution** | Which scheme, from the settlement record | Scheme resolution | Manual review — **never guess** |

### 3.1 The duplicate check is cumulative, not per-claim

The control is not "is this the same claim twice" — it is **has the customer already been made whole on this transaction**:

```
SUM(amounts resolved in the customer's favour on transaction T)
  must not exceed  transaction amount of T
```

This holds even across several partial disputes on the same transaction, and it mirrors the amount chain the schemes enforce on their side.

### 3.2 Scheme resolution — precedence order

| # | Basis | Source |
|---|---|---|
| 1 | Settlement network | The clearing record — **authoritative** |
| 2 | Acquirer reference number | Scheme-encoded in the ARN |
| 3 | BIN / account range | Range table, effective-dated **to the transaction date** |
| 4 | Unresolved | **Route to a human.** A wrong filing burns the time bar |

---

## 4. Stage 3 · PRE-DISPUTE / DEFLECTION *(optional)*

**The cheapest possible outcome.** No filing fee, no analyst time, no scheme clock, no regulatory clock.

| Scheme | Mechanisms |
|---|---|
| **Visa** | Rapid dispute resolution · merchant purchase inquiry · order insight |
| **Mastercard** | Collaboration requests · alert network · consumer clarity |

> ⚠ **A naming trap.** Mastercard's "Collaboration" is this pre-dispute process. Visa's "Collaboration" is one of its two dispute **workflows**. They are unrelated. Never use the word unqualified.

**Exit:** merchant refunds → resolved, no dispute ever filed. Otherwise the case proceeds to provisional credit and filing.

---

## 5. Stage 4 · PROVISIONAL CREDIT

| Property | Detail |
|---|---|
| **Trigger** | The regulatory clock, **not** the scheme |
| **Timing** | Due on its own deadline regardless of scheme progress |
| **Direction** | Issuer → cardholder. **The scheme is not refunding anyone** |
| **Reversal** | **Cannot** be reversed while the investigation is open, and requires advance written notice |

> **This is the most commonly misunderstood step.** Two independent money movements exist: the issuer credits the cardholder under regulation, and the scheme moves the disputed amount between acquirer and issuer under scheme rules. Either can happen without the other.

---

## 6. Stages 5–6 · FILING AND THE ACQUIRER'S RESPONSE

| | **Mastercard (MDR)** | **Visa — Collaboration** | **Visa — Allocation** |
|---|---|---|---|
| Stage 5 name | First Chargeback | Dispute | Dispute |
| Applies to | All reason codes | 12.x processing · 13.x consumer | 10.x fraud · 11.x authorization |
| Who decides validity | The parties | The parties | **Visa**, automatically from its own data |
| Stage 6 name | Second Presentment / Representment | Dispute Response | **— none. The cycle is eliminated** |
| Stage 6 window | 45 days | 30 days — **not** asterisked as hard in Visa's figure | — |
| Evidence model | Documents | Structured compelling-evidence fields | Narrow, enumerated grounds |
| Funds after a decline | Return to acquirer | Return to acquirer | **Stay with the issuer** |

### 6.1 Where the money sits

**The rule: the funds follow the most recent filing — except in Visa Allocation, where they never move at all before the ruling.**

| Event | Visa **Allocation** | Visa **Collaboration** | **Mastercard MDR** |
|---|---|---|---|
| Issuer files the dispute / chargeback | → **Issuer** | → **Issuer** | → **Issuer** |
| Acquirer responds — declines or re-presents | *No such stage.* Funds **stay with the issuer** | → **Acquirer** | → **Acquirer** |
| Pre-arbitration filed | **Acquirer** files · funds **stay with the issuer** | **Issuer** files · funds → **Issuer** | **Issuer** files · *movement unconfirmed* |
| Scheme rules | To the winner | To the winner | To the winner |

**Why Allocation never swaps:** Visa already ruled on validity at stage 5, so the acquirer's pre-arbitration is a challenge to *Visa's* decision — not a re-presentment of the transaction. Nothing moves until Visa decides again.

> **This compounds with provisional credit.** In **Collaboration**, after the acquirer declines and before the issuer files pre-arbitration, the cardholder still holds the credit *and* the disputed funds sit with the acquirer — the issuer is out of pocket on both counts, and cannot reclaim the credit while the investigation is open. In **Allocation** that window never opens.

> ⚠ **A conflict to resolve with your SME.** Pega's material states that in a Collaboration case *"the funds would be with the Acquirer until liability is decided"* — implying no movement at pre-arbitration. The table above reflects the **SME position**: filing pre-arbitration moves the funds back to the issuer. Pega's wording may be describing only the case where the issuer accepts the dispute response and never escalates. Worth confirming against the Visa Core Rules, because it changes the issuer's exposure window materially.

---

## 7. Stage 7 · PRE-ARBITRATION — the filer changes

**This is the most commonly modelled-wrong part of the process.**

| Scheme / workflow | Who files pre-arbitration | Effect on the funds | Why |
|---|---|---|---|
| **Visa — Allocation** | **ACQUIRER** | **None** — funds stay with the issuer | Visa already ruled on validity at stage 5. There is no response stage, so the acquirer's only route to challenge is pre-arbitration |
| **Visa — Collaboration** | **ISSUER** | Funds move **back to the issuer** | Filed after receiving and rejecting the acquirer's dispute response |
| **Mastercard** | **ISSUER** | *Movement unconfirmed* | Always. The acquirer may accept, reject, or take no action |

**The underlying rule:** the party that files is the party dissatisfied with the current state. In Collaboration the acquirer has already responded, so the unhappy party is the issuer. In Allocation there is no response stage, so it is the acquirer. **The filer flips because the sequence flips.**

### 7.1 Sources, and how to verify this yourself

**Both Visa figures have now been read directly. The filing party is settled for both workflows.**

| Source | What it establishes |
|---|---|
| **Visa VCR guide — "Fraud and Authorization" figure** | **Definitive for Allocation.** *Pre-arbitration* runs **Acquirer → Issuer**; *Pre-arbitration Response* runs Issuer → Acquirer; the arbitration connector originates **acquirer-side** |
| **Visa VCR guide — "Consumer and Processing Errors" figure** | **Definitive for Collaboration.** *Dispute* runs Issuer → Acquirer; *Dispute Response* runs Acquirer → Issuer; **_Pre-arbitration_ runs Issuer → Acquirer**; *Pre-arbitration Response* runs Acquirer → Issuer; the arbitration connector originates **issuer-side** |
| **Pega Academy**, Allocation topic | *"the **Acquirer** initiates pre-arbitration against the Issuer"* |
| **Pega Academy**, Collaboration topic | *"The **Issuer** initiates the pre-arbitration against the Acquirer… if the Issuer is not ready to accept the response"* |
| **Rivero** · **Project SME** | Both state and confirm the same |

### 7.2 How to read the Visa figures

The **horizontal party-to-party arrows** are colour-coded by originating party — and read from *our* seat, that colour tells you which integration flow the step belongs to:

| Colour | Visa's meaning — originator | From the issuer's seat | Our integration flow |
|---|---|---|---|
| **Yellow** | **Issuer** originates | **We initiate.** A synchronous call, triggered by a case decision — either an agent action or an automated rule | **1 · CALL / FILE** |
| **Dark blue** | **Acquirer** originates | **It arrives.** We learn of it only by **polling** on a pre-configured schedule | **2 · POLL** |

Side by side, the flip is visible at a glance:

| Step | Allocation | Collaboration | Our flow |
|---|---|---|---|
| Dispute | **Yellow** — issuer | **Yellow** — issuer | **CALL** in both |
| Dispute Response | *stage does not exist* | **Blue** — acquirer | **POLL** *(Collaboration only)* |
| **Pre-arbitration** | **Blue — acquirer** | **Yellow — issuer** | **POLL** in Allocation · **CALL** in Collaboration |
| Pre-arbitration Response | **Yellow** — issuer | **Blue** — acquirer | **CALL** in Allocation · **POLL** in Collaboration |
| Arbitration connector | originates **acquirer**-side | originates **issuer**-side | **POLL** in Allocation · **CALL** in Collaboration |
| Final Ruling | **Yellow** — Visa, out to both parties | **Yellow** — Visa, out to both parties | **POLL** in both |

> **The filer flip is also an integration flip.** The same message type — pre-arbitration — is an outbound call in one workflow and an inbound poll result in the other. The adapter must handle both directions for the same cycle type, which is why `initiatingParty` is a required field and cannot be inferred from the cycle.

**Three caveats when applying the colour rule.**

1. It governs the **horizontal message arrows only**. For the arbitration and final-ruling connectors, the **origin side** — not the colour — identifies the party.
2. **`Final Ruling` is drawn yellow but behaves as a POLL for us.** Visa issues it; we discover it by polling. The colour reflects Visa's diagram convention, not our integration direction.
3. Timeframe asterisks matter: **every window is marked hard except Collaboration's Dispute Response**, which is 30 days without the marker.

> **Read the figures, not the extracted text.** Arrow direction and colour exist only in the rendered image. Extracting the PDF flattens both diagrams into a list in which step order does not survive — in the Collaboration extract, "Pre-arbitration Response" appears *before* "Pre-arbitration", which is impossible as a sequence. That artefact is what made an earlier draft of this document wrongly discount the source.

| Property | Detail |
|---|---|
| Mandatory before arbitration? | **Visa:** yes, both workflows · **Mastercard:** generally, but optional for some categories |
| Partial acceptance | Possible. The remainder is treated as declined; the accepted portion needs its own liability decision |
| No response | Treated as acceptance. **On Visa, silence is acceptance of liability** |

---

## 8. Stages 8–9 · ARBITRATION AND APPEAL

| Property | Detail |
|---|---|
| **Who files arbitration** | Whoever filed pre-arbitration — because arbitration exists only when the other side declined it |
| **Who decides** | **The scheme.** Never the issuer or acquirer |
| **Outcome** | Binding ruling on liability, plus fees to the losing party |
| **Appeal** | Either party, where the disputed amount is at or above the scheme threshold. **The appeal ruling is final** |

> **Appeal is a real stage.** A case can legitimately continue past arbitration — the stage machine must accept it rather than treat it as an invalid transition.

### 8.1 The commercial reality

Losing at arbitration typically costs several times the disputed amount once filing fees, technical fees and analyst time are counted. Write-off thresholds are therefore **effective-dated policy**, owned by the rules capability — not a constant in code.

---

## 9. Parallel and alternate flows

These are **not** stages of the cycle above. Each has independent entry conditions.

| Flow | When it applies | Who initiates | Notes |
|---|---|---|---|
| **Pre-compliance → compliance** | **No** dispute, response or pre-arbitration right exists, **and** a rule violation caused financial loss | Either party | Non-response within the window is treated as full liability |
| **Good faith** | The time bar has **already expired** | Issuer | A voluntary request. No enforcement — hence the name |
| **Recall / withdraw** | The cardholder no longer wishes to pursue, or filed in error | **Only the initiating party**, and only while awaiting the counterparty | Available throughout the lifecycle |

> **Time-bar expiry is not necessarily terminal.** Good faith is the branch that exists afterwards.

---

## 10. Cross-stage concerns

### 10.1 Two clocks, always running

| Clock | Owned by | Behaviour |
|---|---|---|
| **Regulatory** | Compliance & timers | Starts at notice. Usually **shorter** than the scheme clock. Does not pause because the scheme is deliberating |
| **Scheme** | Network exchange | Per cycle, per reason code, effective-dated by ruleset version |

**The regulatory clock frequently expires first.** The bank funds the cardholder while the scheme deliberates — which is why timers must fire even when other capabilities are degraded.

### 10.2 How the platform talks to the scheme

Four flows, not one. Full detail in [architecture §8](./dispute-claims-resolution-architecture.md#8-scheme-integration--the-four-flows).

| Flow | Trigger | Worst failure |
|---|---|---|
| **FILE** | A case decision | Double filing, or a burnt time bar |
| **POLL** | A schedule | **Silent, permanent message loss** if acknowledged before the local commit |
| **FAN-OUT** | A poll result | A poison record blocking good work — one message per case, always |
| **RECONCILE** | A schedule | *This flow is the detector for the other three* |

### 10.3 Controls that must exist at each stage

| Stage | Control |
|---|---|
| Intake | Identity established before a claim exists |
| Triage | Cumulative duplicate check across partial disputes |
| Scheme resolution | Never guess — unresolved routes to a human |
| Filing | Idempotency on `(case, cycle, message type)`; journal before transmit |
| Polling | Persist → commit → **acknowledge**, never reordered |
| Fan-out | One message per case; quarantine carries the original deadline |
| Provisional credit | No reversal while the investigation is open; advance notice required |
| Every stage | An independent reconciliation pass comparing our state to the scheme's |

---

## 11. What this adds to the original stage list

| Added | Why it matters |
|---|---|
| **Complaint as a state before Claim** | Unauthenticated intake cannot start a dispute case. Two regulatory regimes, two clocks |
| **Pre-dispute / deflection as a stage** | The cheapest outcome available, and currently invisible |
| **Provisional credit as an explicit stage** | It is independent of the scheme and on a shorter clock |
| **Visa Allocation has no response stage** | Stage 6 is skipped entirely for fraud and authorization disputes |
| **The pre-arbitration filer changes** | Acquirer in Visa Allocation, issuer everywhere else |
| **Appeal** | A real stage after arbitration |
| **Fund position per stage** | Who holds the disputed money, and when it swaps |
| **Parallel flows** | Compliance, good faith, recall and withdraw are not cycles |

---

## 12. Open questions

1. Does the regulatory clock start at **form submission** or at **identity resolution** for unauthenticated intake?
2. Are CSRs raising a *complaint* record or a *dispute claim*? They are different regimes with different SLAs
3. Current **time bars, response windows and fees** per reason code — needed for every deadline in this document
4. Is the **appeal threshold** regionally variable?
5. Does the current implementation acknowledge to the scheme **before or after** its local commit?
6. Which reason codes genuinely **require customer documents** before filing, and which need only the cardholder statement?
