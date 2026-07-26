# Scoring and Grade Rules

## Contents

- Calculation
- Five positive dimensions
- Risk deduction
- Grade derivation
- Mandatory caps

## Calculation

Calculate:

```text
authenticity
+ business fit
+ purchase signal
+ purchase potential
+ contact execution
+ risk deduction
```

Clamp the result to `0..100`. Score each line item from evidence; never assign a dimension from overall impression.

## 1. Authenticity — 20

| Item | Maximum |
|---|---:|
| Business registry/entity | 6 |
| Website and email | 4 |
| Phone and address | 4 |
| Contact authenticity | 3 |
| Information consistency | 3 |

If the customer has no website and the legal entity cannot be confirmed, this dimension should normally not exceed 8.

## 2. Business fit — 25

| Item | Maximum |
|---|---:|
| Direct industry relevance | 10 |
| Process and application fit | 8 |
| Product entry feasibility | 7 |

If only broad industry relevance is known and no specific process can be confirmed, this dimension should normally not exceed 15.

## 3. Purchase signal — 25

| Item | Maximum |
|---|---:|
| Explicit inquiry or purchase demand | 10 |
| Sample, test, or quotation | 7 |
| Parameters, quantity, or purchase timing | 5 |
| Continued communication or reply | 3 |

With no purchase-related information, score `0..3`. A generic catalog request without a specific requirement normally scores no more than 5 for this entire dimension.

## 4. Purchase potential — 15

| Item | Maximum |
|---|---:|
| Product consumption frequency | 5 |
| Production or channel scale | 5 |
| Repeat purchase likelihood | 3 |
| Alternative supply opportunity | 2 |

Do not award full scale points without reliable scale evidence. Mark product-consumption and repeat-purchase reasoning as inference when it comes from process or maintenance logic rather than purchase records.

## 5. Contact execution — 15

| Item | Maximum |
|---|---:|
| Valid contact method | 5 |
| Relevant contact role | 4 |
| Reply status | 3 |
| Clear next step | 3 |

Seniority does not replace a purchase signal.

## 6. Risk deduction — 0 to -20

| Risk | Suggested deduction |
|---|---:|
| Abnormal, cancelled, or unconfirmed legal entity | -5 to -10 |
| Serious name/address/phone conflict | -3 to -8 |
| Sanctions or export-control risk | -5 to -10 |
| Payment-credit or fraud risk | -3 to -10 |
| Logistics, customs, or transaction-path difficulty | -2 to -5 |
| Clearly abnormal contact information | -2 to -5 |

Cap aggregate risk deduction at `-20`. Use current official lists or reliable sources for sanctions. Never assign sanctions merely because a customer is in Russia, Belarus, or another higher-risk market.

## Grade derivation

### A — Priority development

Normally `80..100`, and all must be true:

- Entity is authentic and information is basically consistent.
- Business fit is high.
- An explicit inquiry, sample, test, quotation, or purchase requirement exists.
- No material entity, payment, sanctions, or compliance risk is present.

Without an explicit purchase signal, never assign A.

### B — Active development

Normally `60..79`, or a score above 79 capped by a missing A condition. The customer is authentic and fits, but quantity, budget, timing, equipment, current brand, or decision process remains unclear.

### C — Low-cost follow-up

Normally `40..59`. Use when fit exists but demand is weak, the contact lacks authority, public information is sparse, or scale is unknown. Simplified mode is normally C unless severe risk or a score below 40 requires D.

### D — Defer

Normally below 40, or use when severe verified entity, sanctions, fraud, payment, or compliance risk requires deferral.

## Mandatory caps

- No explicit purchase signal → maximum B.
- Generic catalog request → usually B or C, not A.
- Large apparent company scale alone → never A.
- Owner/director/engineer title alone → never substitutes for purchase signal.
- No website plus unconfirmed entity → maximum C.
- Authenticity doubtful → never A.
- Simplified mode → normally C or D.
- Use exactly one grade from `A`, `B`, `C`, `D`; never `A-`, `B+`, or multiple grades.

The implementation in `scripts/models.py::derive_grade` is the deterministic source of truth. Excel reproduces the same rules with visible validation formulas.
