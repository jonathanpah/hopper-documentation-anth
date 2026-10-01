# Handoff example

A complete handoff of a fictional conversation. It shows the expected level of detail: complete sentences, exact paths and identifiers, the user's words in quotation marks, and nothing the files or git already show. The program writes the header and the titles; the writer writes the summary and the text of each section.

```markdown
# Handoff: Fix of the shipping cost at checkout

- **Date:** 2026-03-14 18:42:07 +00:00
- **Conversation:** 3f9c2a71-5b8e-4d0a-9c61-2e7f4b1a8d05
- **Working directory:** /home/ana/projects/store
- **Previous handoff of this conversation:** [handoff-20260314-151203-3f9c2a71.md](handoff-20260314-151203-3f9c2a71.md)
- **Trigger:** on request
- **Writer:** claude-sonnet-5-5 with medium effort
- **Last recorded message:** 8d1e0f42-77a3-4c2b-9e15-0b6a2f9c3d81

## Goal

Fix the shipping cost charged on orders above $300.00, which should be zero. The work is done when the tests in `tests/test_shipping.py` pass and the fix is in a commit on the `fix-shipping` branch.

## Topics and current state

- **P1 — Fix of the free shipping rule: completed.** The rule was fixed in `/home/ana/projects/store/shipping/calculation.py`, function `calculate_shipping`. The 14 tests in `tests/test_shipping.py` passed (`pytest` output in the conversation). Commit `a41e9d2` on the `fix-shipping` branch.
- **P2 — Shipping rounding: waiting.** The user will choose between rounding up and rounding to the nearest cent.

## Next step

Waiting for the user's decision on rounding (P2). The user said she will decide tomorrow.

## Decisions and authorizations

- Decision: the free shipping threshold applies to the total after discounts. Reason: it is the rule published on the store's help page.
- Authorization: "You may fix it and commit on the fix-shipping branch". Scope: only the `fix-shipping` branch. Already used in commit `a41e9d2`.

## Constraints in force

- "Do not merge into main or publish anything" — from the user, at the start of the conversation.
- Commit messages in English — the user's preference.

## Findings and discarded approaches

- The error came from comparing against the total before discounts.
- Discarded: moving the rule to `order/total.py`. The user rejected it because other modules import that function.

## Pending items and commitments

- **PD1 — Update `docs/shipping-rules.md`:** the AI's commitment after the P2 decision. Closes when the file reflects the chosen rule. Status: waiting for P2.

## Gaps

- The integration tests in `tests/integration/` were not run; the conversation does not show why.

## How to resume

1. Read this handoff and this folder's `index.md`.
2. Check the real state before acting: the `git log` of the `fix-shipping` branch should show commit `a41e9d2`, and `git status` should be clean.
3. Do not redo the fix or the commit: they are already completed.
4. Ask the user for the rounding decision, if she has not answered yet.
```
