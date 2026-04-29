---
type: knowledge
created: 2026-04-28
scope: reusable-across-weeks
purpose: prevent FX math drift in LLM narration; provide reliable conversion table
---

# FX Reference — THB ↔ USD

Inject this file into Claude's context for any workshop that touches currency. Pre-computed table prevents drift; the constant is the source of truth.

---

## The constant

```
1 USD = 32 THB     (locked for course; any change updates this file only)
1 THB = $0.03125
```

**Rationale for locked rate:** real FX rates fluctuate; for teaching, a fixed constant lets learners reason about magnitudes without rate confusion. Real-world FX is a W6+ topic.

---

## Conversion table (Claude reads this; doesn't compute)

When narrating numbers in either direction, Claude finds the closest row and notes the conversion. Small rounding (±$10 on a $20K number) is acceptable and feels natural.

| THB | USD |
|---:|---:|
| ฿100 | $3 |
| ฿500 | $16 |
| ฿1,000 | $31 |
| ฿2,500 | $78 |
| ฿5,000 | $156 |
| ฿10,000 | $313 |
| ฿25,000 | $781 |
| ฿50,000 | $1,563 |
| ฿100,000 | $3,125 |
| ฿250,000 | $7,813 |
| ฿500,000 | $15,625 |
| ฿756,000 | $23,625 |
| ฿800,000 | $25,000 |
| ฿1,000,000 | $31,250 |
| ฿2,500,000 | $78,125 |
| ฿5,000,000 | $156,250 |
| ฿8,000,000 | $250,000 |
| ฿10,000,000 | $312,500 |

---

## Narration patterns

When stating a number to the learner:

- **Default:** lead with THB, parenthetical USD: *"฿756,000 a year (~$23,600)"*
- **For very small or very large numbers:** state both upfront so magnitude lands
- **For interactive moments:** ask first — *"shall I show numbers in THB only, or both?"* — and remember the answer for the rest of the workshop
- **Round USD to nearest hundred** for large numbers, nearest dollar for small ones — readability over precision

---

## Data layer rules (workshop seed data)

For any seed data containing money:

1. **Original currency preserved** in `amount_original` + `currency` columns
2. **THB normalized** in `amount_thb` column (always present)
3. **USD pre-computed** in `amount_usd` column (always present)
4. Claude reads columns; never converts on the fly

This means:
- Consolidation step: Claude maps original → THB using the constant, fills `amount_thb` and `amount_usd`
- Dashboard: reads pre-computed columns, optionally toggles display
- Narration: references the table above, not arithmetic

---

## Risks to watch

- **LLM still gets math wrong sometimes** even with the table. Mitigation: tell Claude in the SCRIPT.md to *"reference the FX table when stating converted amounts; do not compute conversions inline."* The dashboard does the real math; Claude just reads.
- **Rate change after course launches:** update this single file. All references resolve.
- **Mixed-currency rows in seed data:** every workshop's data spec must explicitly note currency for every transaction.

---

## When this file changes

Update if:
- The constant changes
- A workshop introduces a new currency (add a section)
- Drift incidents in dry-runs reveal the table needs more rows

Then update [CLAUDE.md](../CLAUDE.md).
